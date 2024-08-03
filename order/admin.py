from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
from .serializers import OrderSerializer  # Import OrderSerializer

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'chat_id')
    search_fields = ('phone', 'chat_id')


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
    list_display = ['id', 'status', 'last_updated']
    readonly_fields = ['id', 'name', 'surname', 'phone', 'email', 'receiver', 'receiver_comments', 'total_quantity', 'total_price', 'submitted_at', 'created_at',  'processed_at', 'complete_at', 'canceled_at', 'chat_id']
    fields = [
        'id', 'name', 'surname', 'phone', 'email', 'address', 'receiver', 'receiver_comments', 
        'present', 'status', 'total_quantity', 'total_price', 'submitted_at','created_at',  'processed_at', 'complete_at', 'canceled_at'
    ]
    inlines = [OrderItemInline]

    def last_updated(self, obj):
        return obj.last_updated
    last_updated.short_description = 'Last Updated'

    def total_quantity(self, obj):
        return sum(item.quantity for item in obj.order_items.all())
    total_quantity.short_description = 'Total Quantity'

    def total_price(self, obj):
        return sum(item.quantity * item.product.price for item in obj.order_items.all())
    total_price.short_description = 'Total Price'

#    def get_queryset(self, request):
#        qs = super().get_queryset(request)
#        for order in qs:
#            if order.status == 'created' and not order.created_at:
#                order.created_at = timezone.now()
#                order.save(update_fields=['created_at'])
 #       return qs


    def save_model(self, request, obj, form, change):
        if change:  # Only if we're editing an existing record
            old_obj = self.model.objects.get(pk=obj.pk)
            if old_obj.status != obj.status or old_obj.status == obj.status:
                # Update fields based on the new status
                if obj.status == 'processed':
                    obj.processed_at = timezone.now()
                elif obj.status == 'complete':
                    obj.complete_at = timezone.now()
                elif obj.status == 'canceled':
                    obj.canceled_at = timezone.now()
                # Add more conditions if needed

        # Call the parent class's save_model method
        super().save_model(request, obj, form, change)
        
admin.site.register(Order, OrderAdmin)