from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
from .serializers import OrderSerializer  # Import OrderSerializer
import json
from django.utils.html import format_html

@admin.register(OrderSummary)
class OrderSummaryAdmin(admin.ModelAdmin):
    list_display = ('chat_id',)
    search_fields = ('chat_id',)
    readonly_fields = ('order_summary_pretty',)

    def order_summary_pretty(self, obj):
        # Ensure 'orders' is the correct field name
        return format_html('<pre>{}</pre>', json.dumps(obj.orders, indent=2, ensure_ascii=False))

    order_summary_pretty.short_description = 'Order Summary (JSON)'

    fieldsets = (
        (None, {
            'fields': ('chat_id', 'order_summary_pretty')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        # Add 'chat_id' to readonly fields when editing an existing object
        if obj:
            return self.readonly_fields + ('chat_id',)
        return self.readonly_fields

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

class TelegramUserFilter(admin.SimpleListFilter):
    title = 'chat_id'
    parameter_name = 'chat_id'

    def lookups(self, request, model_admin):
        # Create a list of distinct phone numbers with chat_ids
        telegram_users = TelegramUser.objects.all()
        return [
            (f"{user.phone} - {user.chat_id}", f"{user.chat_id}")
            for user in telegram_users
        ]

    def queryset(self, request, queryset):
        if self.value():
            phone, chat_id = self.value().split(' - ')
            return queryset.filter(telegram_user__phone=phone, telegram_user__chat_id=chat_id)
        return queryset


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'last_updated', 'phone', 'chat_id']
    readonly_fields = ['id', 'name', 'surname', 'phone', 'email', 'receiver', 'receiver_comments', 'total_quantity', 'total_price', 'submitted_at', 'created_at', 'processed_at', 'complete_at', 'canceled_at', 'chat_id']
    fields = [
        'id', 'name', 'surname', 'phone', 'email', 'address', 'receiver', 'receiver_comments',
        'present', 'status', 'total_quantity', 'total_price', 'submitted_at', 'created_at', 'processed_at', 'complete_at', 'canceled_at'
    ]
    list_filter = [
        'status',
        'phone',  # Add filtering by phone directly
        TelegramUserFilter,  # Add custom filter for TelegramUser
        'created_at',
        'processed_at',
        'complete_at',
        'canceled_at',
        'present',
    ]
    search_fields = ['phone', 'email', 'name', 'surname']
    inlines = [OrderItemInline]
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Use prefetch_related for related fields if needed
        return qs.prefetch_related('telegram_user')
    def chat_id(self, obj):
        return obj.chat_id if obj.chat_id else None
    chat_id.short_description = 'Chat ID'

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
                if obj.status == 'submited':
                    obj.submitted_at = timezone.now()
                if obj.status == 'created':
                    obj.created_at = timezone.now()
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