from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Collection
from dotenv import load_dotenv
import os
from distutils.util import strtobool

load_dotenv()

AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_MEDIA_LOCATION = os.getenv('AWS_MEDIA', 'media')  # Default to 'media' if not specified
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_MEDIA_LOCATION}/'
USE_S3 = bool(strtobool(os.getenv('USE_S3', 'True')))

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag', 'photo']
    readonly_fields = ['image_tag']
    actions = ['delete_selected']

    def image_tag(self, obj):
        if obj.photo:
            photo_url = MEDIA_URL + obj.photo.name if USE_S3 else obj.photo.url
            print(photo_url)  # For debugging
            return format_html(f'<img src="{photo_url}" width="100" />')
        else:
            return '(No image)'

    image_tag.short_description = "Image"
    image_tag.allow_tags = True

    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection', 'image_tag', 'price', 'stock', 'available', 'photo')
    readonly_fields = ['image_tag']
    actions = ['delete_selected']

    def image_tag(self, obj):
        if obj.photo:
            photo_url = MEDIA_URL + obj.photo.name if USE_S3 else obj.photo.url
            print(photo_url)  # For debugging
            return format_html(f'<img src="{photo_url}" width="100" />')
        else:
            return '(No image)'

    image_tag.short_description = "Image"
    image_tag.allow_tags = True
