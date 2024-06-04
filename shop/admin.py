from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Category, Collection, Product, ProductImage

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
    list_display = ('id', 'get_product_name', 'first_product_image', 'collection', 'price', 'currency', 'stock', 'available', 'sales_count', 'popularity')
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
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />', first_image.images.url)
        elif obj.photo:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />', obj.photo.url)
        else:
            placeholder_url = 'sample.png'
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />', placeholder_url)
    first_product_image.short_description = 'Image'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'get_image_url', 'display_photo']
    readonly_fields = ['get_image_url', 'display_photo']

    def get_image_url(self, obj):
        if obj.images:
            return obj.images.url
        return "No Image Found"
    get_image_url.short_description = 'Image URL'

    def display_photo(self, obj):
        if obj.images:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />'.format(obj.images.url))
        return "No Image Found"
    display_photo.short_description = "Photo"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ['id', 'name']

admin.site.register(Category, CategoryAdmin)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_collection_name_link', 'category', 'image_tag')
    search_fields = ['name']
    readonly_fields = ('id', 'image_tag')

    def get_collection_name_link(self, obj):
        return format_html('<a href="{}">{}</a>', reverse("admin:shop_collection_change", args=(obj.id,)), obj.name)
    get_collection_name_link.short_description = "Collection"

    def image_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:150px; max-width:150px;" />', obj.photo.url)
        return format_html('<img src="{}" style="max-height:150px; max-width:150px;" />', 'placeholder.jpg')
    image_tag.short_description = "Image"

admin.site.register(Collection, CollectionAdmin)
