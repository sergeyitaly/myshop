from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.template.defaultfilters import truncatechars 
import os
from storages.backends.s3boto3 import S3Boto3Storage
from dotenv import load_dotenv
from distutils.util import strtobool
from django.utils.html import format_html


load_dotenv()
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_MEDIA_LOCATION = os.getenv('AWS_MEDIA', 'media')  # Default to 'media' if not specified
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
USE_S3 = bool(strtobool(os.getenv('USE_S3', 'True')))
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_MEDIA_LOCATION}/'
    
class MediaStorage(S3Boto3Storage):
    location = os.getenv('AWS_MEDIA', 'media')  # Default to 'media' if not specified
    file_overwrite = True

class Collection(models.Model):
    if USE_S3:
        photo = models.ImageField(upload_to="photos/collection", storage=MediaStorage(), null=True, blank=True)
    else:    
        photo = models.ImageField(upload_to="photos/collection", null=True, blank=True)
    
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'

    @property
    def short_description(self):
        return truncatechars(self.description, 20)    
    
    def image_tag(self, obj):
        if obj.photo:
            if USE_S3: photo_url = MEDIA_URL + obj.photo.name
            else: photo_url = obj.photo.url
            print(photo_url)
            return format_html(f'<img src="{photo_url}" width="100" />')
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
    if USE_S3:
        photo = models.ImageField(upload_to="photos/product", storage=MediaStorage(), null=True, blank=True)
        brandimage = models.FileField(upload_to="photos/svg", storage=MediaStorage(), null=True, blank=True) 
    else:    
        photo = models.ImageField(upload_to="photos/product", null=True, blank=True)
        brandimage = models.FileField(upload_to="photos/svg", null=True, blank=True)
    
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='products')
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

    @property
    def short_description(self):
        return truncatechars(self.description, 20)    
    
    def image_tag(self, obj):
        if obj.photo:
            if USE_S3: photo_url = MEDIA_URL + obj.photo.name
            else: photo_url = obj.photo.url
            print(photo_url)
            return format_html(f'<img src="{photo_url}" width="100" />')
        else:
            return '(No image)'    
    image_tag.short_description = "Image"
    image_tag.allow_tags = True

    def delete(self, *args, **kwargs):
        # Delete associated photo when product is deleted
        if self.photo:
            self.photo.delete()
        super().delete(*args, **kwargs)
