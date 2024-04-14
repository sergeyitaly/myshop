from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Collection
from django.conf import settings

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag', 'photo']
    readonly_fields = ['image_tag']

    actions = ['delete_selected']

    def image_tag(self, obj):
        if obj.photo:
            if settings.USE_S3:
                photo_url = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{settings.AWS_MEDIA_LOCATION}/{obj.photo.name}'
            else:
                photo_url = obj.photo.url
            return format_html(f'<img src="{photo_url}" width="100" />')
        else:
            return '(No image)'

    image_tag.short_description = "Image"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection', 'image_tag', 'price', 'stock', 'available', 'photo')
    readonly_fields = ['image_tag']

    actions = ['delete_selected']

    def image_tag(self, obj):
        if obj.photo:
            if settings.USE_S3:
                photo_url = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{settings.AWS_MEDIA_LOCATION}/{obj.photo.name}'
            else:
                photo_url = obj.photo.url
                print(photo_url)
            return format_html(f'<img src="{photo_url}" width="100" />')
        else:
            return '(No image)'

    image_tag.short_description = "Image"
