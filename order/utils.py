from django.utils import timezone
from order.models import Order
from .notifications import update_order_status_with_notification
from django.utils.dateformat import format as date_format
from django.db import transaction
from order.models import OrderSummary


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
                            'orders': order_summary["order_items"],
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

    # Gather status timestamps
    status_fields = {
        'submitted_at': order.submitted_at,
        'created_at': order.created_at,
        'processed_at': order.processed_at,
        'complete_at': order.complete_at,
        'canceled_at': order.canceled_at,
    }

    # Find the latest status timestamp
    latest_status_field = max(
        status_fields,
        key=lambda k: status_fields[k] or timezone.datetime.min
    )
    latest_status_timestamp = status_fields[latest_status_field]

    # Prepare the order summary
    order_summary = {
        "order_id": order.id,
        "order_items": order_items_data,
        "submitted_at": date_format(order.submitted_at, 'Y-m-d H:i') if order.submitted_at else None,
    }

    # Format timestamps to include only hours and minutes
    for field in ['created_at', 'processed_at', 'complete_at', 'canceled_at']:
        if status_fields[field]:
            order_summary[field] = date_format(status_fields[field], 'Y-m-d H:i')
        else:
            order_summary[field] = None

    # Add the latest status timestamp to the summary
    if latest_status_timestamp:
        order_summary[latest_status_field] = date_format(latest_status_timestamp, 'Y-m-d H:i')

    return order_summary
