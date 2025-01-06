from celery import shared_task
from django.utils import timezone
from order.utils import update_orders
from order.notifications import update_order_status_with_notification
from order.models import Order

@shared_task
def update_order_statuses():
    now = timezone.now()
    submitted_to_created = update_orders('submitted', 'created', 1, 'submitted_at', now, Order)
    for order in submitted_to_created:
        update_order_status_with_notification(
            order_id=order.id,
            order_items=order.order_items.all(),
            new_status='created',
            status_field='created_at',
            chat_id=order.telegram_user.chat_id,
            language=order.language,
        )
    created_to_processed = update_orders('created', 'processed', 20, 'created_at', now, Order)
    for order in created_to_processed:
        update_order_status_with_notification(
            order_id=order.id,
            order_items=order.order_items.all(),
            new_status='processed',
            status_field='processed_at',
            chat_id=order.telegram_user.chat_id,
            language=order.language,
        )
    processed_to_complete = update_orders('processed', 'complete', 24 * 60, 'processed_at', now, Order)
    for order in processed_to_complete:
        update_order_status_with_notification(
            order_id=order.id,
            order_items=order.order_items.all(),
            new_status='complete',
            status_field='completed_at',
            chat_id=order.telegram_user.chat_id,
            language=order.language,
        )

    return {
        'submitted_to_created': len(submitted_to_created),
        'created_to_processed': len(created_to_processed),
        'processed_to_complete': len(processed_to_complete),
    }
