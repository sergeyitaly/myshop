from django.contrib import admin
from django.forms import FileField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Category, Collection, Product, ProductImage
from django.utils.html import format_html
from django.urls import reverse

class CustomImageFileField(FileField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators = [validate_image]

def validate_image(value):
    valid_extensions = ['jpg', 'jpeg', 'png', 'svg']
    ext = value.name.split('.')[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError(_('Only JPG, JPEG, PNG, and SVG files are allowed.'))

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    readonly_fields = ['get_image_tag']

    def get_image_tag(self, obj):
        if obj.images:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />', obj.images.url)
        return "No Image Found"
    get_image_tag.short_description = 'Image'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('get_product_name', 'first_product_image', 'collection', 'price', 'currency', 'stock', 'available', 'sales_count', 'popularity')
    search_fields = ['name']
    readonly_fields = ('id', 'slug', 'image_tag')
    fields = (
        'id', 'name', 'collection', 'description', 'price', 'currency', 'stock', 'available', 'sales_count',
        'popularity', 'color', 'size', 'slug', 'photo', 'image_tag'
    )
    list_display_links = ['get_product_name']
    sortable_by = ['collection', 'price', 'sales_count', 'popularity']
    show_full_result_count = False  # Hide the count of total results

    def get_product_name(self, obj):
        return format_html('<a href="{}">{}</a>', reverse("admin:shop_product_change", args=(obj.id,)), obj.name)
    get_product_name.short_description = 'Name'

    def first_product_image(self, obj):
        first_image = obj.productimage_set.first()  # Use the related manager
        if first_image and first_image.images:
            print(first_image.images.url)  # Add this line to print the URL

            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />', first_image.images.url)
        return 'No Image Found'
    first_product_image.short_description = 'Image'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image_tag']
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        if obj.images:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />', obj.images.url)
        return "No Image Found"
    image_tag.short_description = 'Image'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ['id', 'name']

admin.site.register(Category, CategoryAdmin)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'image_tag')
    search_fields = ['name']
    readonly_fields = ('id', 'image_tag')

    def image_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:150px; max-width:150px;" />', obj.photo.url)
        return 'No Image Found'
    image_tag.short_description = "Image"

admin.site.register(Collection, CollectionAdmin)
