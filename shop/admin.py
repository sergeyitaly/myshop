from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Product, Collection
from dotenv import load_dotenv
import os
from django.conf import settings

load_dotenv()

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag','photo']
    readonly_fields = ['image_tag']

    actions = ['delete_selected']

    def image_tag(self, obj):
        if obj.photo:
            USE_S3 = os.getenv('USE_S3') == 'TRUE'
            if USE_S3:  photo_url = settings.MEDIA_URL + obj.photo.name
            else:   photo_url = obj.photo.url
            print(photo_url)
            return format_html(f'<img src="{photo_url}" width="100" />')
        else:
            return '(No image)'   
    image_tag.short_description = "Image"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection', 'image_tag', 'price', 'stock', 'available','photo')
    readonly_fields = ['image_tag']

    actions = ['delete_selected']

    def image_tag(self, obj):
        if obj.photo:
            USE_S3 = os.getenv('USE_S3')=='TRUE'
            if USE_S3:  photo_url = settings.MEDIA_URL + obj.photo.name
            else:   photo_url = obj.photo.url
            print(photo_url)
            return format_html(f'<img src="{photo_url}" width="100" />')
        else:
            return '(No image)'    
    image_tag.short_description = "Image"
