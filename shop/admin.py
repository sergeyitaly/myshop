from django.contrib import admin
from .models import Category, Collection, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ['name']
    readonly_fields = ('image_tag',)

admin.site.register(Collection, CollectionAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection', 'price', 'stock', 'available')
    search_fields = ['name']
    readonly_fields = ('image_tag',)
    fields = ('name', 'collection', 'price', 'stock', 'available', 'slug')  # Added 'slug' field here

admin.site.register(Product, ProductAdmin)
