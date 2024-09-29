#order/utils.py

from django.utils import timezone
from order.models import Order
from .notifications import update_order_status_with_notification

def update_order_statuses():
    now = timezone.now()
    update_submitted_to_created(now)
    update_created_to_processed(now)
    update_processed_to_complete(now)

def update_submitted_to_created(now):
    orders = Order.objects.filter(status='submitted')
    for order in orders:
        submitted_at = order.submitted_at
        if submitted_at and (now - submitted_at).total_seconds() / 60 >= 1:
            chat_id = order.telegram_user.chat_id if order.telegram_user else None
            if chat_id:
                update_order_status_with_notification(order.id, order.order_items, 'created', 'created_at', chat_id)


def update_created_to_processed(now):
    orders = Order.objects.filter(status='created')
    for order in orders:
        created_at = order.created_at
        if created_at and (now - created_at).total_seconds() / 60 >= 20:
            chat_id = order.chat_id  # Use the property defined in Order model
            if chat_id:
                update_order_status_with_notification(order.id, order.order_items, 'processed', 'processed_at', chat_id)

def update_processed_to_complete(now):
    orders = Order.objects.filter(status='processed')
    for order in orders:
        processed_at = order.processed_at
        if processed_at and (now - processed_at).total_seconds() / 3600 >= 24:
            chat_id = order.telegram_user.chat_id if order.telegram_user else None
            if chat_id:
                update_order_status_with_notification(order.id, order.order_items, 'complete', 'complete_at', chat_id)
