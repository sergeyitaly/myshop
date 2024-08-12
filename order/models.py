from django.db import models
from shop.models import Product
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import logging
import decimal
from django.utils.translation import gettext_lazy as _


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
        # Call the parent class's save method
        super().save(*args, **kwargs)
                # Update or create the OrderSummary record
        if self.chat_id:
            order_summary, created = OrderSummary.objects.get_or_create(chat_id=self.chat_id)
            orders = order_summary.orders or []
            order_data = {
                'order_id': self.id,
                'status': self.status,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'processed_at': self.processed_at.isoformat() if self.processed_at else None,
                'complete_at': self.complete_at.isoformat() if self.complete_at else None,
                'canceled_at': self.canceled_at.isoformat() if self.canceled_at else None,
            }
            orders.append(order_data)
            order_summary.orders = order_summary._convert_decimals(orders)
            order_summary.save()

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

    
