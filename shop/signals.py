from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from shop.models import Product
from order.models import OrderItem

@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
@receiver(post_save, sender=Product)
def update_product_availability(sender, instance, **kwargs):
    if sender == Product:
        if instance.stock <= 0:
            if instance.available:
                instance.available = False
                instance.save(update_fields=["available"])
        else:
            if not instance.available:
                instance.available = True
                instance.save(update_fields=["available"])
