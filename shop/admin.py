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


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    form = ProductForm
    list_display = ('id_link', 'name', 'collection', 'main_product_image', 'price', 'currency', 'discount', 'stock', 'available', 'sales_count', 'popularity')
    search_fields = ['name']
    readonly_fields = ('id', 'slug', 'main_product_image_display', 'display_gallery')
    fields = (
        'id', 'name', 'collection', 'description', 'price', 'currency', 'discount', 'stock', 'available', 'sales_count',
        'popularity', 'color_name', 'color_value', 'size', 'slug', 'photo',
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


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('id', 'name')
    search_fields = ['name']


@admin.register(Collection)
class CollectionAdmin(TranslationAdmin):
    form = CollectionForm
    list_display = ('id', 'name', 'category', 'image_tag')
    search_fields = ['name']
    readonly_fields = ('id', 'image_tag')

    def image_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:150px; max-width:150px;" />'.format(obj.photo_thumbnail.url))
        else:
            return format_html('<img src="{}" style="max-height:150px; max-width:150px;" />'.format('collection.jpg'))
    image_tag.short_description = _("Image")

# Register admin classes for translated models, handling potential errors
def register_translation_admin(model, admin_class):
    try:
        admin.site.register(model, admin_class)
    except NotRegistered:
        admin.site.register(model, admin.ModelAdmin)

@admin.register(AdditionalField)
class AdditionalFieldAdmin(TranslationAdmin):
    list_display = ('name', 'value')
    search_fields = ('name', 'value')