from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import APILog

@receiver(post_save, sender=APILog)
def recalculate_request_sum_on_create(sender, instance, created, **kwargs):
    if created:
        total_requests = APILog.objects.filter(endpoint=instance.endpoint).count()
        APILog.objects.filter(endpoint=instance.endpoint).update(request_sum=total_requests)

@receiver(post_delete, sender=APILog)
def recalculate_request_sum_on_delete(sender, instance, **kwargs):
    total_requests = APILog.objects.filter(endpoint=instance.endpoint).count()
    APILog.objects.filter(endpoint=instance.endpoint).update(request_sum=total_requests)
