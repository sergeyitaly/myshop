from django.db import models
from django.utils.text import slugify
from django.template.defaultfilters import truncatechars 
from django.utils.html import format_html
import os
from storages.backends.s3boto3 import S3Boto3Storage
from dotenv import load_dotenv
from distutils.util import strtobool

load_dotenv()
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_MEDIA_LOCATION = os.getenv('AWS_MEDIA', 'media')
USE_S3 = bool(strtobool(os.getenv('USE_S3', 'True')))
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{AWS_MEDIA_LOCATION}/'

class MediaStorage(S3Boto3Storage):
    location = AWS_MEDIA_LOCATION
    file_overwrite = True
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, db_index=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug if it's not set
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    

class Collection(models.Model):
    if USE_S3:
        photo = models.ImageField(upload_to="photos/collection", storage=MediaStorage(), null=True, blank=True)
    else:    
        photo = models.ImageField(upload_to="photos/collection", null=True, blank=True)
        
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=False, null=False)  # Make description required
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sales_count = models.PositiveIntegerField(default=0)  # Field to track sales
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, db_index=True)


    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format(self.image.url))
        else:
            return 'No Image Found'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug if it's not set
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        # Delete associated photo when product is deleted
        if self.photo:
            self.photo.delete()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    image_tag.short_description = "Image"
    image_tag.allow_tags = True


class Product(models.Model):
    if USE_S3:
        photo = models.ImageField(upload_to="photos/product", storage=MediaStorage(), null=True, blank=True)
        brandimage = models.FileField(upload_to="photos/svg", storage=MediaStorage(), null=True, blank=True) 
    else:    
        photo = models.ImageField(upload_to="photos/product", null=True, blank=True)
        brandimage = models.FileField(upload_to="photos/svg", null=True, blank=True)

    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=False, null=False)  # Make description required
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sales_count = models.PositiveIntegerField(default=0)  # Field to track sales
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, db_index=True)


    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format(self.image.url))
        else:
            return 'No Image Found'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug if it's not set
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        # Delete associated photo when product is deleted
        if self.photo:
            self.photo.delete()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    image_tag.short_description = "Image"
    image_tag.allow_tags = True