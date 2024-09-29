from django.utils import timezone
from order.models import Order
from .notifications import update_order_status_with_notification

def update_order_statuses():
    now = timezone.now()

    # Update statuses
    update_submitted_to_created(now)
    update_created_to_processed(now)
    update_processed_to_complete(now)

def get_order_summary(order):
    """
    Helper function to format order summary in the required format.
    """
    return {
        "order_id": order.id,
        "order_items": [
            {
                "size": item.size,
                "quantity": item.quantity,
                "total_sum": float(item.total_sum),
                "color_name": item.color.name,
                "item_price": "{:.2f}".format(item.item_price),
                "color_value": item.color.value,
                "product_name": item.product.name,
                "collection_name": item.product.collection.name if item.product.collection else None
            }
            for item in order.order_items.all()
        ],
        "processed_at": order.processed_at.strftime("%Y-%m-%d %H:%M") if order.processed_at else None,
        "submitted_at": order.submitted_at.strftime("%Y-%m-%d %H:%M") if order.submitted_at else None
    }

def update_submitted_to_created(now):
    orders = Order.objects.filter(status='submitted')
    for order in orders:
        submitted_at = order.submitted_at
        if submitted_at and (now - submitted_at).total_seconds() / 60 >= 1:
            chat_id = order.telegram_user.chat_id if order.telegram_user else None
            if chat_id:
                order_summary = get_order_summary(order)
                update_order_status_with_notification(order.id, order_summary, 'created', 'created_at', chat_id)

def update_created_to_processed(now):
    orders = Order.objects.filter(status='created')
    for order in orders:
        created_at = order.created_at
        if created_at and (now - created_at).total_seconds() / 60 >= 20:
            chat_id = order.telegram_user.chat_id if order.telegram_user else None
            if chat_id:
                order_summary = get_order_summary(order)
                update_order_status_with_notification(order.id, order_summary, 'processed', 'processed_at', chat_id)

def update_processed_to_complete(now):
    orders = Order.objects.filter(status='processed')
    for order in orders:
        processed_at = order.processed_at
        if processed_at and (now - processed_at).total_seconds() / 3600 >= 24:
            chat_id = order.telegram_user.chat_id if order.telegram_user else None
            if chat_id:
                order_summary = get_order_summary(order)
                update_order_status_with_notification(order.id, order_summary, 'complete', 'complete_at', chat_id)
