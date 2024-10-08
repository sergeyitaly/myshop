from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductImage, Category, Collection, AdditionalField
from .forms import AdditionalFieldForm, ProductForm, CollectionForm, ProductImageForm
from django.utils.translation import gettext_lazy as _  # Import gettext_lazy for translations
from modeltranslation.admin import TranslationAdmin

from modeltranslation.translator import translator, NotRegistered
from .translator import *  # Ensure this is imported
from django.urls import reverse


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    form = ProductImageForm
    extra = 1
    verbose_name = _('Product Image')
    verbose_name_plural = _('Product Images')

class AdditionalFieldInline(admin.TabularInline):
    model = AdditionalField
    form = AdditionalFieldForm
    extra = 1
    verbose_name = _('Additional Field')
    verbose_name_plural = _('Additional Fields')
    fields = ('name_en', 'name_uk','value_en', 'value_uk')



@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    form = ProductForm
    list_display = ('id_link', 'name','collection', 'main_product_image', 'price', 'currency', 'discount', 'stock', 'available', 'sales_count', 'popularity')
    search_fields = ['name_en', 'name_uk']
    readonly_fields = ('id', 'slug', 'main_product_image_display', 'display_gallery')
    fields = (
        'id', 'name', 'id_name', 'collection', 'description_en','description_uk', 'price', 'currency', 'discount', 'stock', 'available', 'sales_count',
        'popularity', 'color_name_en','color_name_uk', 'color_value', 'size', 'slug', 'photo',
        'main_product_image_display', 'display_gallery'
    )
    list_display_links = ['name']
    sortable_by = ['category','collection', 'price', 'sales_count', 'popularity']
    show_full_result_count = False
    inlines = [ProductImageInline, AdditionalFieldInline]

    def id_link(self, obj):
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name),  args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.id)
    id_link.short_description = 'ID'

    def main_product_image(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />'.format(obj.photo.url))
        else:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />'.format('product.png'))
    main_product_image.short_description =_('Main Image')

    def main_product_image_display(self, obj):
        return self.main_product_image(obj)
    main_product_image_display.short_description = _('Main Image Preview')
    main_product_image_display.allow_tags = True

    def display_gallery(self, obj):
        images_html = ""
        product_images = obj.productimage_set.all()
        for image in product_images:
            if image.images:
                images_html += format_html('<img src="{}" style="max-width:100px; max-height:100px; margin-right: 10px;" />'.format(image.images.url))
        return format_html(images_html)
    display_gallery.short_description = _("Product Images")

    def save_model(self, request, obj, form, change):
        # Call the parent class's save_model method to ensure normal behavior
        super().save_model(request, obj, form, change)

        # Generate id_name only if the product has an ID and name
        if obj.id and obj.name:
            # Replace spaces with underscores in the name
            name_with_underscores = obj.name.replace(' ', '_')
            obj.id_name = f"{obj.id}_{name_with_underscores}"
            # Save the product instance again to update id_name
            obj.save(update_fields=['id_name'])

class CollectionInline(admin.TabularInline):
    model = Collection
    form = CollectionForm
    extra = 1
    verbose_name = _('Collection')
    verbose_name_plural = _('Collections')
    fields = ('name', 'category', 'photo', 'image_tag')
    readonly_fields = ('id', 'image_tag')

    def image_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:100px; max-width:100px;" />'.format(obj.photo_thumbnail.url))
        else:
            return format_html('<img src="{}" style="max-height:100px; max-width:100px;" />'.format('collection.jpg'))
    image_tag.short_description = _("Image")



@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'collections_with_products')
    search_fields = ['name_en', 'name_uk']
    inlines = [CollectionInline]

    def collections_with_products(self, obj):
        collections = Collection.objects.filter(category=obj)
        collections_html = ''
        for collection in collections:
            collection_link = reverse('admin:%s_%s_change' % (collection._meta.app_label, collection._meta.model_name), args=[collection.pk])
            
            # Display collection photo directly
            collection_photo_html = ''
            if collection.photo:
                collection_photo_html = format_html('<img src="{}" style="max-height:50px; max-width:50px; margin-right: 10px;" />', collection.photo.url)
            else:
                collection_photo_html = format_html('<img src="{}" style="max-height:50px; max-width:50px; margin-right: 10px;" />', 'collection.jpg')

            collections_html += format_html('<div style="display: flex; align-items: center;">{}</div>', 
                                            format_html('{}<h4><a href="{}">{}</a></h4>', collection_photo_html, collection_link, collection.name))
            
            products = Product.objects.filter(collection=collection)
            products_html = '<ul>'
            for product in products:
                product_link = reverse('admin:%s_%s_change' % (product._meta.app_label, product._meta.model_name), args=[product.pk])
                products_html += format_html('<li><a href="{}">{}</a></li>', product_link, product.name)
            products_html += '</ul>'
            
            collections_html += products_html
            
        return format_html(collections_html)
    
    
    collections_with_products.short_description = _('Collections and Products')


class ProductInline(admin.TabularInline):
    model = Product
    form = ProductForm
    extra = 1
    verbose_name = _('Product')
    verbose_name_plural = _('Products')
    fields = (
        'name_en', 'name_uk', 'description_en', 'description_uk', 'price', 'currency', 'discount', 'stock', 'available', 
        'sales_count', 'popularity', 'color_name_en', 'color_name_uk', 'color_value', 'size', 'photo', 'product_image'
    )
    readonly_fields = ('product_image',)

    def product_image(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:50px; max-width:50px;" />', obj.photo.url)
        else:
            return format_html('<img src="{}" style="max-height:50px; max-width:50px;" />', 'product.png')
    product_image.short_description = _('Product Image')

@admin.register(Collection)
class CollectionAdmin(TranslationAdmin):
    form = CollectionForm
    list_display = ('id', 'name', 'category', 'image_tag', 'products_list')
    search_fields = ['name_en','name_uk']
    readonly_fields = ('id', 'image_tag')
    inlines = [ProductInline]

    def image_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:150px; max-width:150px;" />'.format(obj.photo_thumbnail.url))
        else:
            return format_html('<img src="{}" style="max-height:150px; max-width:150px;" />'.format('collection.jpg'))
    image_tag.short_description = _("Image")

    def display_gallery(self, obj):
        images_html = ""
        product_images = obj.productimage_set.all()
        for image in product_images:
            if image.images:
                images_html += format_html('<img src="{}" style="max-height:30px; max-width:30px; margin-left:5px;" />'.format(image.images.url))
        return format_html(images_html)
    display_gallery.short_description = _("Product Images")

    def products_list(self, obj):
        products = Product.objects.filter(collection=obj)
        products_html = '<ul>'
        for product in products:
            product_link = reverse('admin:%s_%s_change' % (product._meta.app_label, product._meta.model_name), args=[product.pk])
            main_photo_url = product.photo.url if product.photo else 'product.png'
            # Use display_gallery to get additional images
            additional_images_html = self.display_gallery(product)
            products_html += format_html(
                '<li><a href="{}">{}</a> <img src="{}" style="max-height:50px; max-width:50px; margin-left:5px;" /> {} </li>',
                product_link, product.name, main_photo_url, additional_images_html
            )
        products_html += '</ul>'
        return format_html(products_html)

    products_list.short_description = _('Products')

# Register admin classes for translated models, handling potential errors
def register_translation_admin(model, admin_class):
    try:
        admin.site.register(model, admin_class)
    except NotRegistered:
        admin.site.register(model, admin.ModelAdmin)
