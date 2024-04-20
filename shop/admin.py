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
    list_display = ('name', 'category','display_photo','display_description', 'display_price', 'stock', 'available')
    readonly_fields = ['slug']  # Make slug readonly

    # Specify the fields to display and edit in the admin form
    fields = ['name', 'description', 'category','photo', 'price', 'currency', 'stock', 'available', 'slug']
    
    def display_price(self, obj):
        return f'{obj.currency} {obj.price}'

    display_price.short_description = 'Price'
    
    def display_image(self, obj):
        if obj.photo:
            return '<img src="{}" style="max-height: 50px; max-width: 50px;" />'.format(obj.photo.url)
        else:
            return 'No Image Found'

    display_image.short_description = 'Image'
    display_image.allow_tags = True  # Required for HTML rendering in Django admin
    
    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />'.format(obj.photo.url))
        else:
            return 'No Image Found'

    display_photo.short_description = 'Photo Preview'
    def save_model(self, request, obj, form, change):
        """Automatically generate the slug when saving a new product."""
        if not obj.slug:  # Generate slug only if it's not set
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)

    def display_description(self, obj):
        if obj.description:
            return obj.description[:150] + '...' if len(obj.description) > 150 else obj.description
        else:
            return 'No Description'

    display_description.short_description = 'Description'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_photo','display_description','display_price', 'stock', 'available')
    readonly_fields = ['slug']  # Make slug readonly

    # Specify the fields to display and edit in the admin form
    fields = ['name', 'description', 'photo', 'price', 'currency','stock', 'available', 'slug']
    
    def display_price(self, obj):
        return f'{obj.currency} {obj.price}'

    display_price.short_description = 'Price'
    
    def save_model(self, request, obj, form, change):
        """Automatically generate the slug when saving a new product."""
        if not obj.slug:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)
        
    def display_image(self, obj):
        if obj.photo:
            return '<img src="{}" style="max-height: 50px; max-width: 50px;" />'.format(obj.photo.url)
        else:
            return 'No Image Found'

    display_image.short_description = 'Image'
    display_image.allow_tags = True  # Required for HTML rendering in Django admin

    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />'.format(obj.photo.url))
        else:
            return 'No Image Found'

    display_photo.short_description = 'Photo Preview'
    
    def save_model(self, request, obj, form, change):
        """Automatically generate the slug when saving a new product."""
        if not obj.slug:  # Generate slug only if it's not set
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)
        
    def display_description(self, obj):
        if obj.description:
            return obj.description[:150] + '...' if len(obj.description) > 150 else obj.description
        else:
            return 'No Description'

    display_description.short_description = 'Description'