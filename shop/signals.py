from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from shop.models import Product
from order.models import OrderItem
from django_redis import get_redis_connection
from celery.signals import task_postrun

@task_postrun.connect
def close_redis_connection(sender=None, **kwargs):
    # Close the Redis connection after each task completes
    redis_conn = get_redis_connection('default')
    redis_conn.close()

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
