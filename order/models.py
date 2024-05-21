from django.db import models

# Define the order model
class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    # Renamed the 'order' field to 'parent_order' to avoid conflicts
    parent_order = models.ForeignKey('self', on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.id}"

    class Meta:
        ordering = ('-submitted_at',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

# Define the order item model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
