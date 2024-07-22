# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductImage, Category, Collection, AdditionalField
from .forms import AdditionalFieldForm, ProductForm, CollectionForm, ProductImageForm

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    form = ProductImageForm
    extra = 1

class AdditionalFieldInline(admin.TabularInline):
    model = AdditionalField
    form = AdditionalFieldForm
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('id', 'name', 'collection', 'main_product_image', 'price', 'currency', 'discount', 'stock', 'available', 'sales_count', 'popularity')
    search_fields = ['name']
    readonly_fields = ('id', 'slug', 'main_product_image_display', 'display_gallery')
    fields = (
        'id', 'name', 'collection', 'description', 'price', 'currency', 'discount', 'stock', 'available', 'sales_count',
        'popularity', 'color_name', 'color_value', 'size', 'slug', 'photo',
        'main_product_image_display', 'display_gallery'
    )
    list_display_links = ['name']
    sortable_by = ['collection', 'price', 'sales_count', 'popularity']
    show_full_result_count = False
    inlines = [ProductImageInline, AdditionalFieldInline]

    def main_product_image(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />'.format(obj.photo.url))
        else:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />'.format('product.png'))
    main_product_image.short_description = 'Main Image'

    def main_product_image_display(self, obj):
        return self.main_product_image(obj)
    main_product_image_display.short_description = 'Main Image Preview'
    main_product_image_display.allow_tags = True

    def display_gallery(self, obj):
        images_html = ""
        product_images = obj.productimage_set.all()
        for image in product_images:
            if image.images:
                images_html += format_html('<img src="{}" style="max-width:100px; max-height:100px; margin-right: 10px;" />'.format(image.images.url))
        return format_html(images_html)
    display_gallery.short_description = "Product Images"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['name']
    readonly_fields = ('id', 'name')

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    form = CollectionForm
    list_display = ('id', 'name', 'category', 'image_tag')
    search_fields = ['name']
    readonly_fields = ('id', 'image_tag')

    def image_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:150px; max-width:150px;" />'.format(obj.photo.url))
        else:
            return format_html('<img src="{}" style="max-height:150px; max-width:150px;" />'.format('collection.jpg'))
    image_tag.short_description = "Image"