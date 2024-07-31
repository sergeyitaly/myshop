from django.db import models
from shop.models import Product
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

class TelegramUser(models.Model):
    phone = models.CharField(max_length=15, unique=True)  # Store phone numbers
    chat_id = models.CharField(max_length=255, unique=True)  # Store chat IDs

    def __str__(self):
        return f'{self.phone} - {self.chat_id}'
    
from django.db import models
from django.utils import timezone

class Order(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('created', 'Created'),
        ('processed', 'Processed'),
        ('complete', 'Complete'),
        ('canceled', 'Canceled'),
    )

    name = models.CharField(max_length=100, default='Default Name')
    surname = models.CharField(max_length=100, default='Default Surname')
    phone = models.CharField(max_length=20, help_text='Contact phone number')
    email = models.EmailField()
    address = models.TextField(null=True, blank=True)
    receiver = models.BooleanField(null=True, help_text='Other person')
    receiver_comments = models.TextField(blank=True, null=True, help_text='Comments about the receiver')
    submitted_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(null=True, blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    complete_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='submitted')
    parent_order = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    present = models.BooleanField(null=True, help_text='Package as a present')

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
        return None

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

    class Meta:
        ordering = ('-submitted_at',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total_sum = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
