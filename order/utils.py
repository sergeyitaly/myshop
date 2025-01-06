from django.utils import timezone
from order.models import Order
from datetime import timedelta
from celery import shared_task
from django.db import transaction

@shared_task
def update_order_statuses():
    now = timezone.now()

    def update_orders(current_status, new_status, minutes, status_field):
        threshold_time = now - timedelta(minutes=minutes)
        with transaction.atomic():  
            orders_to_update = Order.objects.filter(
                status=current_status,
                **{f"{status_field}__lte": threshold_time}
            )
            updated_count = orders_to_update.update(
                status=new_status,
                **{f"{new_status}_at": now}
            )
        return updated_count

    submitted_to_created = update_orders(
        current_status='submitted',
        new_status='created',
        minutes=1,
        status_field='submitted_at'
    )

    created_to_processed = update_orders(
        current_status='created',
        new_status='processed',
        minutes=20,
        status_field='created_at'
    )

    processed_to_complete = update_orders(
        current_status='processed',
        new_status='complete',
        minutes=24 * 60,
        status_field='processed_at'
    )

    return {
        'submitted_to_created': submitted_to_created,
        'created_to_processed': created_to_processed,
        'processed_to_complete': processed_to_complete,
    }
