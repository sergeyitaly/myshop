from asyncio import format_helpers
from django.contrib import admin
from django.urls import reverse
from .models import Product, Collection

class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag',]
    fields = ['name','slug','image_tag','photo' ]
    readonly_fields = ['slug','image_tag']
 
    def delete(self, obj):
        view_name = "admin:{}_{}_delete".format(obj._meta.app_label,obj._meta.model_name)
        link = reverse(view_name, args=[Product.pk])
        html = '<input type="button" onclick="location.href=\'{}\'" value="Delete" />'.format(link)
        return format_helpers(html)

admin.site.register(Collection, CollectionAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection','image_tag', 'price', 'stock',)
    fields = ['name', 'slug','collection','image_tag', 'photo','image_brand','brandimage','color','price', 'stock','description']
    readonly_fields = ['slug','image_tag','image_brand']
    list_filter = ('collection','available',)
    save_on_top = True      
  

    def delete(self, obj):
        view_name = "admin:{}_{}_delete".format(obj._meta.app_label,obj._meta.model_name)
        link = reverse(view_name, args=[Product.pk])
        html = '<input type="button" onclick="location.href=\'{}\'" value="Delete" />'.format(link)
        return format_helpers(html)


admin.site.register(Product, ProductAdmin)
admin.site.site_header = 'Admin panel'