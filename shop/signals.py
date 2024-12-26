
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from order.models import OrderItem

@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_product_availability(sender, instance, **kwargs):
    product = instance.product
    if product.stock <= 0:
        product.available = False
    else:
        product.available = True
    product.save()
