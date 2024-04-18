from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Collection, Category
from django.utils.text import slugify  # Import slugify function

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']  # Define fields to search on

    list_display = ['name', 'slug']
    #readonly_fields = ['slug']
    actions = ['delete_selected']

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'category','image_tag',  'price', 'stock', 'available','photo']
    readonly_fields = ['image_tag']
    actions = ['delete_selected']
    list_filter = ('category','available',)

    def image_tag(self, obj):
        if obj.photo:
            photo_url = obj.photo.url
            print(photo_url)  # For debugging
            return format_html(f'<img src="{photo_url}" width="100" />')
        else:
            return '(No image)'

    image_tag.short_description = "Image"
    image_tag.allow_tags = True

    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag', 'price', 'stock', 'available', 'photo')
    readonly_fields = ['image_tag']
    actions = ['delete_selected']

    def image_tag(self, obj):
        if obj.photo:
            photo_url = obj.photo.url
            print(photo_url)  # For debugging
            return format_html(f'<img src="{photo_url}" width="100" />')
        else:
            return '(No image)'

    image_tag.short_description = "Image"
    image_tag.allow_tags = True
