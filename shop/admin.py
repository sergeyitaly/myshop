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
            return format_html('<img src="{}" width="100" />'.format(obj.photo.url))
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
            print(obj.photo.url)
            return format_html('<img src="{}" width="100" />'.format(obj.photo.url))
        else:
            return '(No image)'

    image_tag.short_description = "Image"
