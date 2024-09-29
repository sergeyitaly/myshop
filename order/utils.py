from django.utils import timezone
from order.models import Order
from .notifications import update_order_status_with_notification
from rest_framework.response import Response

def update_order_statuses():
    now = timezone.now()
    update_orders('submitted', 'created', 1, 'submitted_at', now)
    update_orders('created', 'processed', 20, 'created_at', now)
    update_orders('processed', 'complete', 24 * 60, 'processed_at', now)

def update_orders(current_status, new_status, threshold_minutes, timestamp_field, now):
    orders = Order.objects.filter(status=current_status)
    for order in orders:
        order_timestamp = getattr(order, timestamp_field)
        if order_timestamp and (now - order_timestamp).total_seconds() / 60 >= threshold_minutes:
            chat_id = order.telegram_user.chat_id if order.telegram_user else None
            if chat_id:
                update_order_status(order, new_status, now, timestamp_field)
                notify_user_with_order_status(order, new_status, chat_id)

def update_order_status(order, new_status, now, timestamp_field):
    order.status = new_status
    setattr(order, f'{new_status}_at', now)  # Dynamically set the timestamp for the new status
    order.save()

def notify_user_with_order_status(order, new_status, chat_id):
    order_items_data = [
        {
            "size": item.size,
            "quantity": item.quantity,
            "total_sum": item.total_sum,
            "color_name": item.color_name,
            "item_price": item.item_price,
            "color_value": item.color_value,
            "product_name": item.product_name,
            "collection_name": item.collection_name,
        }
        for item in order.order_items.all()
    ]
    
    update_order_status_with_notification(
        order.id,
        order_items_data,
        new_status,
        f'{new_status}_at',
        chat_id
    )
