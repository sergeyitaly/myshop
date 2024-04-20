from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Collection, Category
from django.utils.text import slugify


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'slug']
    readonly_fields = ['slug']
    actions = ['delete_selected']
    

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category','price', 'stock', 'available', 'created', 'updated', 'display_image')
    readonly_fields = ['slug']

    # Specify the fields to display and edit in the admin form
    fieldsets = [
        (None, {'fields': ['name', 'description', 'photo', 'price', 'stock', 'available']}),
        ('Slug', {'fields': ['slug'], 'classes': ['collapse']}),
    ]

    # Prepopulate the slug field based on the name field
    prepopulated_fields = {'slug': ('name',)}

    def display_image(self, obj):
        if obj.photo:
            return '<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format(obj.photo.url)
        else:
            return 'No Image Found'

    display_image.short_description = 'Image'
    display_image.allow_tags = True  # Required for HTML rendering in Django admin

    def save_model(self, request, obj, form, change):
        """Automatically generate the slug when saving a new product."""
        if not obj.slug:  # Generate slug only if it's not set
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'available', 'created', 'updated', 'display_image')
    readonly_fields = ['slug']

    # Specify the fields to display and edit in the admin form
    fieldsets = [
        (None, {'fields': ['name', 'description', 'photo', 'price', 'stock', 'available']}),
        ('Slug', {'fields': ['slug'], 'classes': ['collapse']}),
    ]

    # Prepopulate the slug field based on the name field
    prepopulated_fields = {'slug': ('name',)}

    def display_image(self, obj):
        if obj.photo:
            return '<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format(obj.photo.url)
        else:
            return 'No Image Found'

    display_image.short_description = 'Image'
    display_image.allow_tags = True  # Required for HTML rendering in Django admin

    def save_model(self, request, obj, form, change):
        """Automatically generate the slug when saving a new product."""
        if not obj.slug:  # Generate slug only if it's not set
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)