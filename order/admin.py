from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['product', 'quantity', 'item_price', 'subtotal']

    def item_price(self, obj):
        return obj.product.price
    item_price.short_description = 'Price'

    def subtotal(self, obj):
        return obj.quantity * obj.product.price
    subtotal.short_description = 'Subtotal'

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = ['name', 'email', 'address', 'total_quantity', 'total_price']

    def total_quantity(self, obj):
        return sum(item.quantity for item in obj.order_items.all())
    total_quantity.short_description = 'Total Quantity'

    def total_price(self, obj):
        return sum(item.quantity * item.product.price for item in obj.order_items.all())
    total_price.short_description = 'Total Price'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('order_items__product')

admin.site.register(Order, OrderAdmin)
