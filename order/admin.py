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
from .utils import send_mass_message_with_logging 

@admin.register(TelegramMessage)
class TelegramMessageAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at', 'get_sent_users')
    actions = ['send_mass_message_with_logging_action']

    # Display the users that the message was sent to
    def get_sent_users(self, obj):
        return ", ".join([user.phone for user in obj.sent_to.all()]) or "No users"
    get_sent_users.short_description = "Sent to"

    # Define the custom action to send mass messages with logging
    def send_mass_message_with_logging_action(self, request, queryset):
        for message in queryset:
            send_mass_message_with_logging(message)  # Call the function for each selected message
        self.message_user(request, "Mass message sent successfully!")
    send_mass_message_with_logging_action.short_description = "Send mass message to selected Telegram messages"

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
    readonly_fields = ['product_photo', 'product_name', 'collection_name', 'size', 'color', 'price','currency']

    def product_photo(self, obj):
        if obj.product.photo:
            return mark_safe(f'<img src="{obj.product.photo.url}" style="width: 50px; height: 50px; object-fit: cover;" />')
        return 'No Image'
    product_photo.short_description = _('Product Photo')

    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = _('Product Name')


    def price(self, obj):
        return obj.product.price
    price.short_description = _('Price')

    def currency(self, obj):
        return obj.product.currency
    currency.short_description = _('Currency')

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
    list_display = ['id', 'status', 'last_updated', 'phone', 'telegram_user_chat_id','language']
    list_filter = [
        'status', 'phone', 'created_at', 'processed_at', 'complete_at', 
        'canceled_at', 'present',
    ]
    search_fields = ['phone', 'email', 'name', 'surname']
    inlines = [OrderItemInline]
    readonly_fields = [
        'id', 'name', 'surname', 'phone', 'email', 'total_quantity', 'total_price', 
        'submitted_at', 'created_at', 'processed_at', 'complete_at', 
        'canceled_at', 'chat_id', 'display_receiver', 'display_receiver_comments'
    ]
    fields = [
        'id', 'language','name', 'surname', 'phone', 'email', 'address', 'receiver', 
        'receiver_comments', 'congrats', 'present', 'status', 'total_quantity', 
        'total_price', 'delivery','payment','submitted_at', 'created_at', 'processed_at', 
        'complete_at', 'canceled_at'
    ]

    def display_receiver(self, obj):
        return "Yes" if obj.receiver else "No"
    display_receiver.short_description = "Receiver"

    def display_receiver_comments(self, obj):
        return obj.receiver_comments or "No comments"
    display_receiver_comments.short_description = "Receiver Comments"

    def telegram_user_chat_id(self, obj):
        return obj.telegram_user.chat_id if obj.telegram_user else "No chat ID"  # Handle None case
    telegram_user_chat_id.admin_order_field = 'telegram_user__chat_id'  # Enable ordering by chat_id
    telegram_user_chat_id.short_description = 'Telegram Chat ID'  # Column header in admin

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('order_items')

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
            
            if old_obj.status != obj.status:
                status_timestamps = {
                    'submitted': 'submitted_at',
                    'created': 'created_at',
                    'processed': 'processed_at',
                    'complete': 'complete_at',
                    'canceled': 'canceled_at',
                }

                # Get the corresponding timestamp field for the status
                status_field = status_timestamps.get(obj.status)
                if status_field:
                    setattr(obj, status_field, timezone.now())

                order_items = obj.order_items.all()

                # If there's a telegram user and chat_id, send a notification
                if obj.telegram_user and obj.telegram_user.chat_id:
                    update_order_status_with_notification(
                        obj.id,
                        order_items,
                        obj.status,
                        status_field,
                        obj.telegram_user.chat_id,
                        obj.language
                    )
                else:
                    logger.warning(f"Telegram user or chat_id is missing for order {obj.id}")

        super().save_model(request, obj, form, change)




# Register the Order model
admin.site.register(Order, OrderAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(OrderSummary, OrderSummaryAdmin)
