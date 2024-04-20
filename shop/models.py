from django.db import models
from django.utils.text import slugify
from django.template.defaultfilters import truncatechars 
from django.utils.html import format_html
import os
from django.core.exceptions import ValidationError
from storages.backends.s3boto3 import S3Boto3Storage
from dotenv import load_dotenv
from distutils.util import strtobool
from PIL import Image
from io import BytesIO
import base64
from django.forms import FileField, ClearableFileInput  # Import necessary forms



load_dotenv()
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_MEDIA_LOCATION = os.getenv('AWS_MEDIA', 'media')
USE_S3 = bool(strtobool(os.getenv('USE_S3', 'True')))
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{AWS_MEDIA_LOCATION}/'

class MediaStorage(S3Boto3Storage):
    location = AWS_MEDIA_LOCATION
    file_overwrite = True

class FlexibleImageField(models.ImageField):
    description = "A flexible image field that supports multiple image types including SVG."
    
    def __init__(self, *args, **kwargs):
        self.use_s3_storage = USE_S3
        if self.use_s3_storage:
            kwargs['storage'] = MediaStorage()
        kwargs['null'] = True
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)
        
    def validate_svg_image(self, image_data):
        # Validate SVG content
        if not image_data.startswith('<svg'):
            raise ValidationError("Invalid SVG content.")

    def validate_image_type(self, image_data):
        # Check if the image data is a valid image (non-SVG)
        try:
            # Decode base64 image data and open it with PIL
            img = Image.open(BytesIO(base64.b64decode(image_data)))
            img.verify()  # Verify image file integrity
        except Exception:
            raise ValidationError("Invalid image content.")

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if value:
            # Access the file via value.file and read the content
            image_data = value.file.read()

            # Check the type of image based on its content
            if isinstance(image_data, str):  # Check if it's a string (SVG)
                self.validate_svg_image(image_data)
            else:  # Otherwise, assume it's binary data (image)
                self.validate_image_type(image_data)

    def formfield(self, **kwargs):
        # Override formfield method to return None (no form field)
        return None
    
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
class Collection(models.Model):
    photo = models.ImageField(upload_to='photos/collection')
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='collections')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

def __str__(self):
    return self.name

class Meta:
    ordering = ('name',)
    verbose_name = 'Collection'
    verbose_name_plural = 'Collections'

    @property
    def short_description(self):
        # Implement this based on the actual field in your model
        return truncatechars(self.name, 20)  # Change 'name' to the appropriate field
    def image_tag(self):
        if self.photo:
            if self.photo.startswith('<svg'):
                return format_html(self.photo)
            else:
                return format_html('<img src="data:image;base64,{}" width="100" />', self.photo)
        else:
            return '(No image)'  
    image_tag.short_description = "Image"
    image_tag.allow_tags = True

    def delete(self, *args, **kwargs):
        # Delete associated photo when collection is deleted
        if self.photo:
            self.photo.delete()
        super().delete(*args, **kwargs)



class Product(models.Model):
    photo = FlexibleImageField(upload_to="photos/product")

    name = models.CharField(max_length=300, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    @property
    def short_description(self):
        return truncatechars(self.description, 20)    
    
    def image_tag(self):
        if self.photo:
            if self.photo.startswith('<svg'):
                return format_html(self.photo)
            else:
                return format_html('<img src="data:image;base64,{}" width="100" />', self.photo)
        else:
            return '(No image)'  
    image_tag.short_description = "Image"
    image_tag.allow_tags = True

    def delete(self, *args, **kwargs):
        # Delete associated photo when product is deleted
        if self.photo:
            self.photo.delete()
        super().delete(*args, **kwargs)
