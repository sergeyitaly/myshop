from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Collection, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'slug']
    readonly_fields = ['slug']
    actions = ['delete_selected']
    

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category','price', 'stock', 'available', 'created', 'updated','display_image')
    prepopulated_fields = {'slug': ('name',)}
    fields = ['name', 'description', 'price', 'stock', 'available', 'slug','photo']
    readonly_fields = ['slug']
    actions = ['delete_selected','mark_available', 'mark_unavailable']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category')  # Use select_related for better performance

    def get_sales_count(self, obj):
        return obj.sales_count

    get_sales_count.short_description = 'Sales Count'

    # Add actions to set product availability
    actions = ['mark_available', 'mark_unavailable']

    def mark_available(self, request, queryset):
        queryset.update(available=True)

    def mark_unavailable(self, request, queryset):
        queryset.update(available=False)

    mark_available.short_description = 'Mark selected products as available'
    mark_unavailable.short_description = 'Mark selected products as unavailable'
    def display_image(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format(obj.photo.url))
        else:
            return 'No Image Found'

    display_image.short_description = 'Image'
    display_image.allow_tags = True  # Required for HTML rendering in Django admin


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'available', 'created', 'updated','display_image')
    prepopulated_fields = {'slug': ('name',)}
    fields = ['name', 'description', 'price', 'stock', 'available', 'slug','photo']
    readonly_fields = ['slug']
    actions = ['delete_selected', 'mark_available', 'mark_unavailable']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category')  # Use select_related for better performance

    def get_sales_count(self, obj):
        return obj.sales_count

    get_sales_count.short_description = 'Sales Count'

    # Add actions to set product availability
    actions = ['mark_available', 'mark_unavailable']

    def mark_available(self, request, queryset):
        queryset.update(available=True)

    def mark_unavailable(self, request, queryset):
        queryset.update(available=False)

    mark_available.short_description = 'Mark selected products as available'
    mark_unavailable.short_description = 'Mark selected products as unavailable'
    
    def display_image(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format(obj.photo.url))
        else:
            return 'No Image Found'

    display_image.short_description = 'Image'
    display_image.allow_tags = True  # Required for HTML rendering in Django admin