from celery import shared_task
from django.utils import timezone
from order.utils import update_orders
from order.notifications import update_order_status_with_notification
from order.models import Order
import logging

logger = logging.getLogger(__name__)

@shared_task
def update_order_statuses():
    now = timezone.now()

    def send_notification_if_possible(order, new_status, status_field):
        if order.telegram_user and order.telegram_user.chat_id:
            update_order_status_with_notification(
                order_id=order.id,
                order_items=order.order_items.all(),
                new_status=new_status,
                status_field=status_field,
                chat_id=order.telegram_user.chat_id,
                language=order.language,
            )
        else:
            logger.info(f"Order {order.id} has no valid Telegram user or chat_id. Notification skipped.")

    # Update statuses and send notifications if applicable
    submitted_to_created = update_orders('submitted', 'created', 1, 'submitted_at', now, Order)
    for order in submitted_to_created:
        # Update the order status
        order.status = 'created'
        order.created_at = now
        order.save()

        # Attempt to send a Telegram notification
        send_notification_if_possible(order, new_status='created', status_field='created_at')

    created_to_processed = update_orders('created', 'processed', 20, 'created_at', now, Order)
    for order in created_to_processed:
        # Update the order status
        order.status = 'processed'
        order.processed_at = now
        order.save()

        # Attempt to send a Telegram notification
        send_notification_if_possible(order, new_status='processed', status_field='processed_at')

    processed_to_complete = update_orders('processed', 'complete', 24 * 60, 'processed_at', now, Order)
    for order in processed_to_complete:
        # Update the order status
        order.status = 'complete'
        order.completed_at = now
        order.save()

        # Attempt to send a Telegram notification
        send_notification_if_possible(order, new_status='complete', status_field='completed_at')

    return {
        'submitted_to_created': len(submitted_to_created),
        'created_to_processed': len(created_to_processed),
        'processed_to_complete': len(processed_to_complete),
    }
