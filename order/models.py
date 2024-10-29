from django.db import models
from shop.models import Product
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import logging
import decimal
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import is_aware, make_naive
from django.utils.dateparse import parse_datetime
from datetime import datetime

logger = logging.getLogger(__name__)


class TelegramUser(models.Model):
    phone = models.CharField(max_length=15, unique=True, verbose_name=_('Phone'))
    chat_id = models.CharField(max_length=255, unique=True, verbose_name=_('Chat ID'))

    def __str__(self):
        return f'{self.phone} - {self.chat_id}'
    
    class Meta:
        verbose_name = _('Telegram user')
        verbose_name_plural = _('Telegram users')

class Order(models.Model):
    STATUS_CHOICES = (
        ('submitted', _('Submitted')),
        ('created', _('Created')),
        ('processed', _('Processed')),
        ('complete', _('Complete')),
        ('canceled', _('Canceled')),
    )


    name = models.CharField(max_length=100, default=_('Default Name'))
    surname = models.CharField(max_length=100, default=_('Default Surname'))
    phone = models.CharField(max_length=20, help_text=_('Contact phone number'))
    email = models.EmailField()
    address = models.TextField(null=True, blank=True, verbose_name=_('Address'))
    receiver = models.BooleanField(null=True, help_text=_('Other person'))
    receiver_comments = models.TextField(blank=True, null=True, help_text=_('Comments about the receiver'))
    congrats = models.TextField(blank=True, null=True, help_text=_('Congrats'))
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Submitted At'))
    created_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Created At'))
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Processed At'))
    complete_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Complete At'))
    canceled_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Canceled At'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted', db_index=True, verbose_name=_('Status'))
    parent_order = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Parent Order'))
    present = models.BooleanField(null=True, help_text=_('Package as a present'))
    telegram_user = models.ForeignKey(TelegramUser, related_name='orders', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('telegram user'))


    
    @property
    def chat_id(self):
        return self.telegram_user.chat_id if self.telegram_user else None
    
    def __str__(self):
        return f"Order {self.id}"

    @property
    def last_updated(self):
        if self.status == 'canceled':
            return self.canceled_at
        if self.status == 'complete':
            return self.complete_at
        if self.status == 'processed':
            return self.processed_at
        if self.status == 'created':
            return self.created_at
        if self.status == 'submitted':
            return self.submitted_at

    def update_status(self, new_status):
        now = timezone.now()
        if new_status == 'created':
            self.created_at = now
        elif new_status == 'processed':
            self.processed_at = now
        elif new_status == 'complete':
            self.complete_at = now
        elif new_status == 'canceled':
            self.canceled_at = now
        self.status = new_status
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        def ensure_datetime(value):
            """Ensures the value is a datetime object, converting strings if necessary."""
            if isinstance(value, str):
                return parse_datetime(value)
            return value

        def make_aware_if_naive(dt):
            """Converts a naive datetime to aware, using the current timezone."""
            if dt and not is_aware(dt):
                return timezone.make_aware(dt)  # Converts naive to aware
            return dt

        def datetime_to_str(dt):
            """Converts a datetime object to string, handling naive and aware datetimes."""
            if dt:
                dt = make_aware_if_naive(dt)  # Ensure it's aware before formatting
                return dt.strftime('%Y-%m-%d %H:%M')
            return None

        if self.chat_id:
            try:
                # Ensure datetime fields are properly parsed and made aware if naive
                submitted_at = make_aware_if_naive(ensure_datetime(self.submitted_at))
                created_at = make_aware_if_naive(ensure_datetime(self.created_at))
                processed_at = make_aware_if_naive(ensure_datetime(self.processed_at))
                complete_at = make_aware_if_naive(ensure_datetime(self.complete_at))
                canceled_at = make_aware_if_naive(ensure_datetime(self.canceled_at))

                # Create a dictionary for status fields
                status_fields = {
                    'submitted_at': submitted_at,
                    'created_at': created_at,
                    'processed_at': processed_at,
                    'complete_at': complete_at,
                    'canceled_at': canceled_at,
                }

                # Determine the latest status key and time
                latest_status_key = max(
                    status_fields,
                    key=lambda k: status_fields[k] or datetime.min
                )
                latest_status_time = status_fields[latest_status_key]

                # Fetch order items details for the order
                order_items_data = [
                    {
                        "quantity": item.quantity,
                        "total_sum": float(item.total_sum),
                        "color_name": item.color_name,
                        "item_price": str(item.item_price),
                        "color_value": item.color_value,
                        "product_name": item.product.name,
                        "collection_name": item.product.collection.name,
                    }
                    for item in self.order_items.all()
                ]

                # Build the order summary data
                order_data = {
                    "order_id": self.id,
                    "submitted_at": datetime_to_str(submitted_at),
                    latest_status_key: datetime_to_str(latest_status_time),
                    "order_items": order_items_data,
                }

                # Update or create the OrderSummary for the chat_id
                order_summary, created = OrderSummary.objects.get_or_create(chat_id=self.chat_id)
                updated_orders = order_summary.orders or []
                # Save updated order data back to OrderSummary
                order_summary.orders = updated_orders
                order_summary.save()

                logger.info(f"Order summary updated for chat ID {self.chat_id}")

            except Exception as e:
                logger.error(f"Failed to update OrderSummary for chat ID {self.chat_id}: {str(e)}")

    class Meta:
        ordering = ('-submitted_at',)
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')




class OrderSummary(models.Model):
    chat_id = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name=_('Chat ID'))  # Changed to CharField to handle string IDs
    orders = models.JSONField(default=dict, verbose_name=_('Orders'))  # Ensures orders is not null

    def __str__(self):
        return str(self.chat_id)  # Ensure it returns a string representation

    def save(self, *args, **kwargs):
        # Convert Decimal values to float
        self.orders = self._convert_decimals(self.orders)
        super().save(*args, **kwargs)

    def _convert_decimals(self, data):
        if isinstance(data, dict):
            return {key: self._convert_decimals(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._convert_decimals(item) for item in data]
        elif isinstance(data, decimal.Decimal):
            return float(data)
        return data
    
    class Meta:
        verbose_name = _('Order summary')
        verbose_name_plural = _('Order summarys')
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE, verbose_name=_('Order'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name=_('Total Sum'))


    def save(self, *args, **kwargs):
        if self.product:
            self.total_sum = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    
