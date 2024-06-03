from django.contrib import admin
from django.urls import reverse
from .models import Category, Collection, Product, ProductImage
from django.utils.html import format_html

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    readonly_fields = ['product', 'get_image_tag']

    def get_image_tag(self, obj):
        return obj.images.url if obj.images else "No Image Found"
    get_image_tag.short_description = 'Image'
    
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('get_product_name', 'first_product_image', 'collection', 'price', 'currency', 'stock', 'available', 'sales_count', 'popularity')
    search_fields = ['name']
    readonly_fields = ('id', 'slug')
    fields = (
        'id', 'name', 'collection', 'description', 'price', 'currency', 'stock', 'available', 'sales_count',
        'popularity', 'color', 'size', 'slug'
    )
    list_display_links = ['get_product_name']
    sortable_by = ['collection', 'price', 'sales_count', 'popularity']
    show_full_result_count = False  # Hide the count of total results

    def get_product_name(self, obj):
        return format_html('<a href="{}">{}</a>', reverse("admin:shop_product_change", args=(obj.id,)), obj.name)
    get_product_name.short_description = 'Name'

    def first_product_image(self, obj):
        first_image = obj.productimage_set.first()
        if first_image:
            return format_html('<img src="{url}" style="max-width:100px;max-height:100px" />', url=first_image.images.url)
        return 'No Image Found'
    first_product_image.allow_tags = True
    first_product_image.short_description = 'Image'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image_tag']
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        return '<img src="{url}" style="max-width:100px;max-height:100px" />'.format(url=obj.images.url) if obj.images else "No Image Found"
    image_tag.allow_tags = True
    image_tag.short_description = 'Image'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ['id', 'name']

admin.site.register(Category, CategoryAdmin)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'photo')
    search_fields = ['name']
    readonly_fields = ('id',)

admin.site.register(Collection, CollectionAdmin)
