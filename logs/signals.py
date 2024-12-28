from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.core.cache import cache
from .models import IgnoreEndpoint, APILog, APILogExcluded


@receiver(post_save, sender=IgnoreEndpoint)
@receiver(post_delete, sender=IgnoreEndpoint)
def update_ignore_cache(sender, instance, **kwargs):
    ignore_endpoints = IgnoreEndpoint.objects.filter(is_active=True).values_list('name', flat=True)
    cache.set('ignore_endpoints', list(ignore_endpoints))


@receiver(post_save, sender=IgnoreEndpoint)
def move_logs_to_excluded_on_ignore_update(sender, instance, created, **kwargs):
    if instance.is_active:
        exclude_pattern = instance.name.strip()
        if exclude_pattern:
            logs_to_move = APILog.objects.filter(endpoint__contains=exclude_pattern)
            if logs_to_move.exists():
                try:
                    with transaction.atomic():
                        apilog_excluded_entries = [
                            APILogExcluded(endpoint=log.endpoint, timestamp=log.timestamp, request_sum=log.request_sum)
                            for log in logs_to_move
                        ]
                        APILogExcluded.objects.bulk_create(apilog_excluded_entries)
                        logs_to_move.delete()
                except Exception as e:
                    # Log the error (optional, replace with actual logging)
                    print(f'Error moving logs to APILogExcluded for pattern "{exclude_pattern}": {e}')


@receiver(post_save, sender=APILog)
def recalculate_request_sum_on_create(sender, instance, created, **kwargs):
    if created:
        total_requests = APILog.objects.filter(endpoint=instance.endpoint).count()
        APILog.objects.filter(endpoint=instance.endpoint).update(request_sum=total_requests)


@receiver(post_delete, sender=APILog)
def recalculate_request_sum_on_delete(sender, instance, **kwargs):
    total_requests = APILog.objects.filter(endpoint=instance.endpoint).count()
    APILog.objects.filter(endpoint=instance.endpoint).update(request_sum=total_requests)
