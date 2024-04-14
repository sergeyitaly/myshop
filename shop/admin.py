from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Collection
from django.conf import settings

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag']
    readonly_fields = ['image_tag']

    actions = ['delete_selected']

    def image_tag(self, obj):
        if obj.photo:
            USE_S3 = settings.USE_S3 == 'True'  # Convert to boolean
            if USE_S3==True:
                photo_url = settings.MEDIA_URL + obj.photo.name
            else:
                photo_url = obj.photo.url
            return format_html(f'<img src="{photo_url}" width="100" />')
        else:
            return '(No image)'

    image_tag.short_description = "Image"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection', 'image_tag', 'price', 'stock', 'available')
    readonly_fields = ['image_tag']

    actions = ['delete_selected']

    def image_tag(self, obj):
        if obj.photo:
            USE_S3 = settings.USE_S3 == 'True'  # Convert to boolean
            if USE_S3==True:
                photo_url = settings.MEDIA_URL + obj.photo.name
            else:
                photo_url = obj.photo.url
            return format_html(f'<img src="{photo_url}" width="100" />')
        else:
            return '(No image)'

    image_tag.short_description = "Image"
