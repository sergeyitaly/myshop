from django.core.management.base import BaseCommand
from order.tasks import update_order_statuses  # Correct import for tasks
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Trigger order status update"

    def handle(self, *args, **kwargs):
        # Trigger the Celery task to update order statuses
        result = update_order_statuses.apply_async()
        updated_orders_ids = result.result.get('updated_orders_ids', []) if result.result else []

        if updated_orders_ids:
            logger.info(f"Successfully updated statuses for the following order IDs: {', '.join(map(str, updated_orders_ids))}.")
        else:
            logger.warning("No orders found for status update.")
