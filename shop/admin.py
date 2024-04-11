from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Product, Collection

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag']
    readonly_fields = ['image_tag']

    actions = ['delete_selected']

    def image_tag(self, obj):
        if obj.photo:
            return format_html(f'<img src="{obj.photo.url}" width="100" />')
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
            return format_html(f'<img src="{obj.photo.url}" width="100" />')
        else:
            return '(No image)'    
    image_tag.short_description = "Image"
