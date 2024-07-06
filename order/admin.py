# shop/admin.py

from django.contrib import admin
from .models import Order, OrderItem
from .serializers import OrderSerializer

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
    readonly_fields = ['total_quantity', 'total_price']  # Exclude fields managed by serializer
    fields = ['name', 'surname', 'phone', 'email', 'address', 'receiver', 'receiver_comments', 'present']

    def total_quantity(self, obj):
        return sum(item.quantity for item in obj.order_items.all())
    total_quantity.short_description = 'Total Quantity'

    def total_price(self, obj):
        return sum(item.quantity * item.product.price for item in obj.order_items.all())
    total_price.short_description = 'Total Price'

    def save_model(self, request, obj, form, change):
        # Ensure receiver_comments is empty if receiver is False
        if not obj.receiver:
            obj.receiver_comments = ''
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        # Manually save related order items using serializer
        if form.instance.pk is None:
            # Only create order items when creating a new order
            serializer = OrderSerializer(data=form.cleaned_data)
            if serializer.is_valid():
                order = serializer.save()
                form.instance.pk = order.pk
                super().save_related(request, form, formsets, change)

admin.site.register(Order, OrderAdmin)
