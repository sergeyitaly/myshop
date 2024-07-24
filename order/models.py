from django.db import models
from shop.models import Product
from phonenumber_field.modelfields import PhoneNumberField

class TelegramUser(models.Model):
    chat_id = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.phone} - {self.chat_id}"
    

class Order(models.Model):
    name = models.CharField(max_length=100, default='Default Name')
    surname = models.CharField(max_length=100, default='Default Surname')
    phone = PhoneNumberField(null=False, blank=False, help_text='Contact phone number', default='+123456789')
    email = models.EmailField()
    address = models.TextField(null=True, blank=True)
    receiver = models.BooleanField(null=True, help_text='Other person')
    receiver_comments = models.TextField(blank=True, null=True, help_text='Comments about the receiver')  # Added this field
    submitted_at = models.DateTimeField(auto_now_add=True)
    parent_order = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    present = models.BooleanField(null=True, help_text='Package as a present')

    def __str__(self):
        return f"Order {self.id}"

    class Meta:
        ordering = ('-submitted_at',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Reference to the Product model
    quantity = models.PositiveIntegerField()
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Ensure this field exists to store the total sum

    def save(self, *args, **kwargs):
        self.total_sum = self.product.price * self.quantity  # Assuming Product model has a price field
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
