from django.utils import timezone
from order.models import Order, OrderSummary
from .notifications import update_order_status_with_notification
from django.utils.dateformat import format as date_format
from django.db import transaction

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

                # Prepare the order summary
                order_summary = prepare_order_summary(order)

                # Use a transaction to ensure atomicity
                with transaction.atomic():
                    # Check if the OrderSummary already exists
                    order_summary_instance, created = OrderSummary.objects.update_or_create(
                        chat_id=chat_id,
                        defaults={
                            'orders': order_summary["order_items"],  # Ensure this matches your OrderSummary model
                            'latest_status': order_summary["latest_status"],  # Optionally store latest status
                            'latest_status_time': order_summary["latest_status_time"],  # Include latest status timestamp
                        }
                    )

                    # Notify user with the updated order summary
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

def prepare_order_summary(order):
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

    status_mapping = {
        'created': (order.created_at, 'Created'),
        'processed': (order.processed_at, 'Processed'),
        'completed': (order.complete_at, 'Completed'),
        'canceled': (order.canceled_at, 'Canceled'),
    }

    latest_status = None
    latest_status_time = None

    for status, (timestamp, status_name) in status_mapping.items():
        if timestamp:
            if latest_status_time is None or timestamp > latest_status_time:
                latest_status_time = timestamp
                latest_status = status_name

    # Prepare the order summary
    summary = {
        'order_id': order.id,
        'order_items': [
            {
                'size': item['size'],
                'quantity': item['quantity'],
                'total_sum': item['total_sum'],
                'color_name': item['color_name'],
                'item_price': item['item_price'],
                'color_value': item['color_value'],
                'product_name': item['product_name'],
                'collection_name': item['collection_name'],
            } for item in order_items_data
        ],
        'latest_status_name': datetime_to_str(latest_status_time),  # Reflect latest status with its timestamp
        'submitted_at': datetime_to_str(order.submitted_at),  # Convert submitted_at timestamp
    }

    return summary

def datetime_to_str(dt):
    """Convert a datetime object to a formatted string."""
    return date_format(dt, 'Y-m-d H:i') if dt else None
