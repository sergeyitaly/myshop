from django.db import models
from shop.models import Product
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import logging
import decimal
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import make_naive
import datetime

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
    telegram_user = models.ForeignKey(TelegramUser, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Telegram user'))
#    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.SET_NULL, null=True, blank=True)


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
        """Override save method to prevent excessive updates and link Telegram user."""
        # Avoid recursive signal calls by checking if instance has changed
        if self.pk:
            old_instance = Order.objects.get(pk=self.pk)
            if old_instance.status != self.status:
                # Check and link Telegram user only if it's not already set
                if not self.telegram_user and self.phone:
                    try:
                        telegram_user = TelegramUser.objects.get(phone=self.phone)
                        self.telegram_user = telegram_user
                    except TelegramUser.DoesNotExist:
                        self.telegram_user = None
                super().save(*args, **kwargs)  # Only save if status changed
        else:
            # Link Telegram user for new instances
            if not self.telegram_user and self.phone:
                try:
                    telegram_user = TelegramUser.objects.get(phone=self.phone)
                    self.telegram_user = telegram_user
                except TelegramUser.DoesNotExist:
                    self.telegram_user = None
            super().save(*args, **kwargs)  # Save new instance


    class Meta:
        ordering = ('-submitted_at',)
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderSummary(models.Model):
    chat_id = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name=_('Chat ID'))
    orders = models.JSONField(default=dict, verbose_name=_('Orders'))

    def __str__(self):
        return str(self.chat_id)

    def save(self, *args, **kwargs):
        # Ensure the orders field is processed before saving
        self.orders = self._convert_decimals(self.orders)
        super().save(*args, **kwargs)

    def _convert_decimals(self, data):
        if isinstance(data, dict):
            return {key: self._convert_decimals(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._convert_decimals(item) for item in data]
        elif isinstance(data, decimal.Decimal):
            return float(data)
        elif isinstance(data, datetime.datetime):
            return data.isoformat()  # Convert datetime to ISO format
        return data

    class Meta:
        verbose_name = _('Order summary')
        verbose_name_plural = _('Order summaries')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE, verbose_name=_('Order'))
    product = models.ForeignKey(Product, related_name='order_items', verbose_name=_('Product'), on_delete=models.CASCADE)
#    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
  #  product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name=_('Total Sum'))
    language = models.CharField(max_length=2, choices=[('en', 'English'), ('uk', 'Ukrainian')],default='en')
    def save(self, *args, **kwargs):
        if self.product:
            self.total_sum = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
