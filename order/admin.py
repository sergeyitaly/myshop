from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['product', 'quantity']
class OrderItemAdmin(admin.ModelAdmin):
    readonly_fields = ['order', 'quantity']  # Adjust according to your model fields
    list_display = ('order', 'quantity')  # Adjust according to your model fields

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['order', 'quantity']  # Adjust according to your model fields
    extra = 1

admin.site.register(OrderItem, OrderItemAdmin)