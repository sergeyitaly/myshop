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
            instance.available = False
        else:
            instance.available = True
        instance.save()
    elif sender == OrderItem:
        product = instance.product
        if product.stock <= 0:
            product.available = False
        else:
            product.available = True
        product.save()
