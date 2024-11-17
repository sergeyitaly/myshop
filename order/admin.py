from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db.models import Sum, F
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from django.urls import reverse
from .models import *
from .notifications import update_order_status_with_notification
from django.contrib.admin import SimpleListFilter
import json

class OrderSummaryAdmin(admin.ModelAdmin):
    list_display = ('chat_id',)
    search_fields = ('chat_id',)
    readonly_fields = ('order_summary_pretty',)
    list_filter = ('chat_id',)

    def order_summary_pretty(self, obj):
        return format_html('<pre>{}</pre>', json.dumps(obj.orders, indent=2, ensure_ascii=False) if obj.orders else "No data available")
    order_summary_pretty.short_description = _('Order Summary (JSON)')

    fieldsets = (
        (None, {
            'fields': ('chat_id', 'order_summary_pretty')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('chat_id',)
        return self.readonly_fields

    def get_queryset(self, request):
        return super().get_queryset(request)

class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'chat_id')
    search_fields = ('phone', 'chat_id')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_photo', 'product_name', 'collection_name', 'size', 'color', 'total_sum']

    def product_photo(self, obj):
        if obj.product.photo:
            return mark_safe(f'<img src="{obj.product.photo.url}" style="width: 50px; height: 50px; object-fit: cover;" />')
        return 'No Image'
    product_photo.short_description = _('Product Photo')

    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = _('Product Name')

    def collection_name(self, obj):
        return obj.product.collection.name
    collection_name.short_description = _('Collection')

    def size(self, obj):
        if obj.product and hasattr(obj.product, 'size'):
            return obj.product.size
        return 'No Size Available'
    size.short_description = _('Size')


    def color(self, obj):
        return mark_safe(f'<div style="display: flex; align-items: center;"><div style="width: 10px; height: 10px; background-color: {obj.product.color_value}; margin-right: 5px;"></div>{obj.product.color_name}</div>')
    color.short_description = _('Color')

class TelegramUserFilter(SimpleListFilter):
    title = 'chat_id'
    parameter_name = 'chat_id'

    def lookups(self, request, model_admin):
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


class HasOrderItemsFilter(SimpleListFilter):
    title = _('Has Order Items')
    parameter_name = _('has_order_items')

    def lookups(self, request, model_admin):
        return [
            ('yes', _('With Order Items')),
            ('no', _('Without Order Items')),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'yes':
            return queryset.filter(order_items__isnull=False).distinct()
        elif value == 'no':
            return queryset.filter(order_items__isnull=True)
        return queryset


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'last_updated', 'phone', 'chat_id']
    readonly_fields = ['id', 'name', 'surname', 'phone', 'email', 'receiver', 'receiver_comments', 'total_quantity', 'total_price', 'submitted_at', 'created_at', 'processed_at', 'complete_at', 'canceled_at', 'chat_id']
    fields = [
        'id', 'name', 'surname', 'phone', 'email', 'address', 'receiver', 'receiver_comments', 'congrats',
        'present', 'status', 'total_quantity', 'total_price', 'submitted_at', 'created_at', 'processed_at', 'complete_at', 'canceled_at'
    ]
    list_filter = [
        'status',
        'phone',
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
        return qs.prefetch_related('order_items')
    def chat_id(self, obj):
        return obj.chat_id if obj.chat_id else None
    chat_id.short_description = _('Chat ID')

    def last_updated(self, obj):
        return obj.last_updated
    last_updated.short_description = _('Last Updated')

    def total_quantity(self, obj):
        return obj.order_items.aggregate(total=Sum('quantity'))['total'] or 0
    total_quantity.short_description = _('Total Quantity')

    def total_price(self, obj):
        return obj.order_items.aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0
    total_price.short_description = _('Total Price')

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = self.model.objects.get(pk=obj.pk)
            if old_obj.status != obj.status or old_obj.status == obj.status:
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
                order_items = obj.order_items.all()

            # Ensure that obj.telegram_user is not None and has chat_id attribute
            if obj.telegram_user and obj.telegram_user.chat_id:
 # Send notification about status change
                update_order_status_with_notification(
                    obj.id,
                    order_items,
                    obj.status,
                    f'{obj.status}_at',
                    obj.telegram_user.chat_id
                )
        
        super().save_model(request, obj, form, change)

# Register the Order model
admin.site.register(Order, OrderAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(OrderSummary, OrderSummaryAdmin)
