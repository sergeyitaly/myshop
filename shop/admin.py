from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, Collection, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'slug']
    actions = ['delete_selected']
    
    
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'stock', 'available', 'photo']
    readonly_fields = ['photo_display']  # Readonly field for image preview
    list_filter = ['category', 'available']
    search_fields = ['name']

    def photo_display(self, obj):
        if obj.photo:
            return '<img src="{0}" style="max-width: 200px; max-height: 200px;" />'.format(obj.photo.url)
        return '(No SVG)'

    photo_display.short_description = 'SVG Preview'
    photo_display.allow_tags = True

    def delete_selected(self, request, queryset):
        for obj in queryset:
            if obj.photo:
                obj.photo.delete()
            obj.delete()

    delete_selected.short_description = "Delete selected collections"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_thumbnail', 'price', 'stock', 'available', 'photo')
    readonly_fields = ['slug']
    actions = ['delete_selected']
    fields = ['name', 'price', 'stock', 'available', 'photo']  # Include 'photo' field here


    def image_thumbnail(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" />')
        else:
            return '(No image)'

    image_thumbnail.short_description = "Image"

    def delete_selected(self, request, queryset):
        for obj in queryset:
            if obj.photo:
                obj.photo.delete()
            obj.delete()

    delete_selected.short_description = "Delete selected products"
