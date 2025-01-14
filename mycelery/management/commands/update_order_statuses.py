# mycelery/management/commands/update_order_statuses.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from order.utils import update_orders
from order.notifications import update_order_status_with_notification  # Correct import
from order.models import Order, StatusTimePeriod
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Update order statuses and send notifications"

    def handle(self, *args, **kwargs):
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

        # Fetch time periods for the status transitions from the StatusTimePeriod model
        status_time_periods = StatusTimePeriod.objects.all()

        updated_orders = []  # Initialize an empty list to hold the updated orders

        for status_time_period in status_time_periods:
            # Determine the time period to use for the status change
            time_period_in_minutes = status_time_period.custom_time_period if status_time_period.custom_time_period else status_time_period.time_period_in_minutes

            # Update statuses and send notifications if applicable
            orders_to_update = update_orders(
                status_time_period.status_from, 
                status_time_period.status_to, 
                time_period_in_minutes, 
                status_time_period.status_from + '_at', 
                now, 
                Order
            )
            updated_orders.extend(orders_to_update)  # Add updated orders to the list

            # Update the order status dynamically based on the transition
            for order in orders_to_update:
                order.status = status_time_period.status_to
                setattr(order, f"{status_time_period.status_to}_at", now)
                order.save()

                # Attempt to send a Telegram notification
                send_notification_if_possible(order, new_status=status_time_period.status_to, status_field=f"{status_time_period.status_to}_at")

        # Log the result
        logger.info(f"Successfully updated statuses for {len(updated_orders)} orders.")
