from django.utils import timezone
from order.models import Order
from .notifications import update_order_status_with_notification
from django.utils.dateformat import format as date_format

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
                # Update the order status and corresponding timestamp
                update_order_status(order, new_status, now, timestamp_field)

                # Notify user with the updated order summary
                order_summary = prepare_order_summary(order, new_status)
                update_order_status_with_notification(
                    order.id,
                    order_summary["order_items"],
                    new_status,
                    f'{new_status}_at',
                    chat_id
                )

def update_order_status(order, new_status, now, timestamp_field):
    order.status = new_status
    setattr(order, f'{new_status}_at', now)  # Dynamically set the timestamp for the new status
    order.save()

def prepare_order_summary(order, new_status):
    # Prepare order items data
    order_items_data = [
        {
            "size": item.size,
            "quantity": item.quantity,
            "total_sum": item.total_sum,
            "color_name": item.color_name,
            "item_price": str(item.item_price),
            "color_value": item.color_value,
            "product_name": item.product_name,
            "collection_name": item.collection_name,
        }
        for item in order.order_items.all()
    ]
    
    # Dynamically set the status field (e.g., processed_at, submitted_at)
    status_timestamp_field = f'{new_status}_at'
    status_timestamp = getattr(order, status_timestamp_field)
    
    # Prepare the order summary including both submitted_at and current status timestamp
    order_summary = {
        "order_id": order.id,
        "order_items": order_items_data,
        "submitted_at": date_format(order.submitted_at, 'Y-m-d H:i') if order.submitted_at else None,
        status_timestamp_field: date_format(status_timestamp, 'Y-m-d H:i') if status_timestamp else None,
    }
    
    return order_summary
