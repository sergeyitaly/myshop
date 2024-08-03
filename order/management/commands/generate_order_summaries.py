from django.core.management.base import BaseCommand
from order.models import Order, OrderSummary
from order.serializers import OrderSerializer
import logging
from datetime import datetime
from django.utils.timezone import is_aware, make_naive

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Generate order summaries for previously created orders'

    def handle(self, *args, **kwargs):
        try:
            # Fetch all orders with related order items and products
            orders = Order.objects.prefetch_related('order_items__product').all()

            # Group orders by chat_id
            grouped_orders = {}
            for order in orders:
                chat_id = order.telegram_user.chat_id if order.telegram_user else None
                if chat_id not in grouped_orders:
                    grouped_orders[chat_id] = []

                # Convert datetime fields to formatted string
                def datetime_to_str(dt):
                    if dt:
                        # Ensure the datetime is naive for consistent formatting
                        if is_aware(dt):
                            dt = make_naive(dt)
                        return dt.strftime('%Y-%m-%d %H:%M')
                    return None

                # Handle None values and ensure all datetime fields are consistent
                def safe_make_naive(dt):
                    if dt is None:
                        return None
                    return make_naive(dt) if is_aware(dt) else dt

                submitted_at = safe_make_naive(order.submitted_at)
                created_at = safe_make_naive(order.created_at)
                processed_at = safe_make_naive(order.processed_at)
                completed_at = safe_make_naive(order.complete_at)
                canceled_at = safe_make_naive(order.canceled_at)

                # Determine the latest timestamp
                statuses = {
                    'created_at': created_at,
                    'processed_at': processed_at,
                    'completed_at': completed_at,
                    'canceled_at': canceled_at
                }

                latest_status_field = max(
                    statuses,
                    key=lambda s: statuses[s] or datetime.min
                )
                latest_status_timestamp = statuses[latest_status_field]

                # Use the serializer to format the order and items
                serializer = OrderSerializer(order)
                order_data = serializer.data

                # Log the order items for debugging
                logger.info(f'Order {order.id} has {len(order_data["order_items"])} items.')

                # Create order summary with only the required statuses
                summary = {
                    'order_id': order.id,
                    'submitted_at': datetime_to_str(submitted_at),
                    latest_status_field: datetime_to_str(latest_status_timestamp),
                    'order_items': order_data['order_items']
                }

                grouped_orders[chat_id].append(summary)

            # Update OrderSummary
            for chat_id, orders_summary in grouped_orders.items():
                OrderSummary.objects.update_or_create(
                    chat_id=chat_id,
                    defaults={'orders': orders_summary}
                )
                logger.info(f'Order summaries created/updated for chat ID {chat_id}')

        except Exception as e:
            logger.error(f'Error while generating order summaries: {e}')
            self.stderr.write(f'Error while generating order summaries: {e}')
