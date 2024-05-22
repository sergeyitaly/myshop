from django.contrib import admin
from .models import Category, Collection, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    search_fields = ['id','name']

admin.site.register(Category, CategoryAdmin)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'category','photo', 'image_tag') 
    search_fields = ['name']
    readonly_fields = ('id','image_tag',)
    fields = ('id', 'name',  'category', 'photo', 'image_tag','slug') 
admin.site.register(Collection, CollectionAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','photo', 'image_tag','collection', 'price', 'currency', 'stock', 'available', 'sales_count', 'popularity')  # Added 'id' and 'image_tag' here
    search_fields = ['name']
    readonly_fields = ('id', 'slug', 'image_tag')  
    fields = (
        'id', 'name',  'collection', 'description','price', 'currency','stock','available','sales_count',
        'popularity','photo','image_tag','slug'
    ) 

admin.site.register(Product, ProductAdmin)
