from celery import shared_task
from django.utils import timezone
from order.utils import update_orders
from order.notifications import update_order_status_with_notification
from order.models import Order
from order.models import StatusTimePeriod
import logging

logger = logging.getLogger(__name__)

@shared_task
def update_order_statuses():
    now = timezone.now()

    # Fetch time periods for the status transitions from the StatusTimePeriod model
    status_time_periods = StatusTimePeriod.objects.all()
    updated_orders_ids = []  # This will store the IDs of updated orders

    for status_time_period in status_time_periods:
        # Determine the time period to use for the status change
        time_period_in_minutes = status_time_period.custom_time_period if status_time_period.custom_time_period else status_time_period.time_period_in_minutes

        # Update statuses and send notifications if applicable
        updated_orders = update_orders(status_time_period.status_from, status_time_period.status_to, time_period_in_minutes, status_time_period.status_from + '_at', now, Order)

        for order in updated_orders:
            # Update the order status dynamically based on the transition
            order.status = status_time_period.status_to
            setattr(order, f"{status_time_period.status_to}_at", now)
            order.save()

            # Append the order ID to the list of updated orders
            updated_orders_ids.append(order.id)

            # Attempt to send a notification (if needed)
            if order.telegram_user and order.telegram_user.chat_id:
                update_order_status_with_notification(
                    order_id=order.id,
                    order_items=order.order_items.all(),
                    new_status=status_time_period.status_to,
                    status_field=f"{status_time_period.status_to}_at",
                    chat_id=order.telegram_user.chat_id,
                    language=order.language,
                )
            else:
                logger.info(f"Order {order.id} has no valid Telegram user or chat_id. Notification skipped.")
    
    # Log the result with the updated order IDs
    if updated_orders_ids:
        logger.info(f"Successfully updated statuses for orders with IDs: {', '.join(map(str, updated_orders_ids))}.")
    else:
        logger.warning("No orders found for status update.")
    
    return {'updated_orders_ids': updated_orders_ids}  # Return the list of updated order IDs
