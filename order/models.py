from django.db import models
from shop.models import Product
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import decimal
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import make_naive
import datetime
from django.db.models.fields import Field
from django.core.exceptions import ValidationError
from django.conf import settings
import logging, requests

logger = logging.getLogger(__name__)


def send_mass_messages(chat_ids, message):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    
    for chat_id in chat_ids:
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            result = response.json()
            if not result.get('ok'):
                logger.error(f"Failed to send message to {chat_id}: {result.get('description')}")
            else:
                logger.info(f"Message sent to {chat_id}: {result}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send message to {chat_id} due to request error: {e}")



class TelegramUser(models.Model):
    phone = models.CharField(max_length=15, unique=True, verbose_name=_('Phone'))
    chat_id = models.CharField(max_length=255, unique=True, verbose_name=_('Chat ID'))

    def __str__(self):
        return f'{self.phone} - {self.chat_id}'

    class Meta:
        verbose_name = _('Telegram user')
        verbose_name_plural = _('Telegram users')
        
class TelegramMessage(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent_to = models.ManyToManyField('TelegramUser', related_name='sent_messages', blank=True)

    def save(self, *args, **kwargs):
        # Save the instance first to access the ManyToManyField
        super().save(*args, **kwargs)

        # Collect chat IDs from the related TelegramUser instances
        chat_ids = list(self.sent_to.values_list('chat_id', flat=True))

        # Send the message to all chat IDs
        if chat_ids:
            try:
                send_mass_messages(chat_ids, self.content)
                logger.info(f"Message sent to {len(chat_ids)} Telegram users.")
            except Exception as e:
                logger.error(f"Error sending Telegram messages: {e}")

    def __str__(self):
        return f"Message sent on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('submitted', _('Submitted')),
        ('created', _('Created')),
        ('processed', _('Processed')),
        ('complete', _('Complete')),
        ('canceled', _('Canceled')),
    )
    DELIVERY_CHOICES = ( 
        ('self_pickup', _('Self Pickup')), 
        ('nova_poshta', _('Nova Poshta')), 
        ('ukr_poshta', _('Ukr Poshta')), ) 
    PAYMENT_CHOICES = ( 
        ('cash_on_delivery', _('Cash on Delivery')), 
        ('card_online', _('Online Card Payment')), )    
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
    language = models.CharField(max_length=2, choices=[('en', 'English'), ('uk', 'Ukrainian')],default='en')
    delivery = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='self_pickup', verbose_name=_('Delivery Method')) 
    payment = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash_on_delivery', verbose_name=_('Payment Method'))


    def __str__(self):
        return f"Order #{self.id} ({self.name})"

    @property
    def chat_id(self):
        # Ensure chat_id is valid and exists before returning
        if self.telegram_user:
            return self.telegram_user.chat_id
        return None

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
        if self.pk:  # If this is an update (not a new instance)
            old_instance = Order.objects.get(pk=self.pk)
            changes = {}

            for field in self._meta.fields:
                field_name = field.name
                old_value = getattr(old_instance, field_name)
                new_value = getattr(self, field_name)
                
                if old_value != new_value:
                    changes[field_name] = {"old": old_value, "new": new_value}

    #        if changes:
    #            print("Changes detected:", changes)  # Replace with actual logging or handling logic

        # Link Telegram user for new instances or when phone is updated
        if not self.telegram_user and self.phone:
            try:
                telegram_user = TelegramUser.objects.get(phone=self.phone)
                self.telegram_user = telegram_user
            except TelegramUser.DoesNotExist:
                self.telegram_user = None

        # Save the instance
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        if self.product:
            self.total_sum = self.quantity * self.product.price
        super().save(*args, **kwargs)

        
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    def get_product_name(self):
        """Get the product name in the specified language."""
        return getattr(self.product, f'name_{self.language}', self.product.name)

    def get_color_name(self):
        """Get the color name in the specified language."""
        return getattr(self.product, f'color_name_{self.language}', self.product.color_name)

    def get_collection_name(self):
        """Get the collection name in the specified language."""
        return getattr(self.product, f'collection_name_{self.language}', self.product.collection_name)

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

        
class StatusTimePeriod(models.Model):
    STATUS_CHOICES = [
        ('submitted', _('Submitted')),
        ('created', _('Created')),
        ('processed', _('Processed')),
        ('complete', _('Complete')),
    ]

    status_from = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name=_("Status From"),
    )
    status_to = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name=_("Status To"),
    )
    time_period_in_minutes = models.PositiveIntegerField(
        choices=[
            (5, _('5 minutes')),
            (20, _('20 minutes')),
            (24 * 60, _('24 hours')),
        ],
        default=5,
        blank=True,
        null=True,
        verbose_name=_("Predefined Time Period (in minutes)"),
    )
    custom_time_period = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Custom Time Period (in minutes)"),
    )

    class Meta:
        verbose_name = _("Status Time Period")
        verbose_name_plural = _("Status Time Periods")

    def clean(self):
        # Ensure at least one of the two fields is provided
        if not self.time_period_in_minutes and not self.custom_time_period:
            raise ValidationError(
                _("Either a predefined time period or a custom time period must be set.")
            )

    def __str__(self):
        if self.custom_time_period:
            return _(
                "Change from %(status_from)s to %(status_to)s in %(time)s minutes"
            ) % {
                'status_from': self.status_from,
                'status_to': self.status_to,
                'time': self.custom_time_period,
            }
        return _(
            "Change from %(status_from)s to %(status_to)s in %(time)s minutes"
        ) % {
            'status_from': self.status_from,
            'status_to': self.status_to,
            'time': self.time_period_in_minutes,
        }