from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Order, OrderItem
from .serializers import OrderSerializer  # Import OrderSerializer

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['product_photo', 'product_name', 'collection_name', 'quantity', 'size', 'color', 'item_price', 'subtotal']

    def product_photo(self, obj):
        return mark_safe(f'<img src="{obj.product.photo.url}" style="width: 50px; height: 50px; object-fit: cover;" />')
    product_photo.short_description = 'Фото продукту'

    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = 'Назва продукту'

    def collection_name(self, obj):
        return obj.product.collection.name
    collection_name.short_description = 'Колекція'

    def size(self, obj):
        return obj.product.size
    size.short_description = 'Розмір'

    def color(self, obj):
        return mark_safe(f'<div style="display: flex; align-items: center;"><div style="width: 10px; height: 10px; background-color: {obj.product.color_value}; margin-right: 5px;"></div>{obj.product.color_name}</div>')
    color.short_description = 'Колір'

    def item_price(self, obj):
        return obj.product.price
    item_price.short_description = 'Ціна'

    def subtotal(self, obj):
        return obj.quantity * obj.product.price
    subtotal.short_description = 'Subtotal'


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = ['id', 'name', 'surname', 'phone', 'email', 'receiver', 'receiver_comments', 'submitted_at', 'present', 'total_quantity', 'total_price']
    fields = [
        'id', 'name', 'surname', 'phone', 'email', 'address', 'receiver', 'receiver_comments', 
        'present', 'submitted_at', 'total_quantity', 'total_price'
    ]  # Include all necessary fields

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
