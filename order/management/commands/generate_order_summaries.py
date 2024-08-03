# yourapp/management/commands/generate_order_summaries.py

from django.core.management.base import BaseCommand
from order.models import Order, OrderItem, OrderSummary
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Generate order summaries for previously created orders'

    def handle(self, *args, **kwargs):
        # Fetch all orders with related order items and products
        orders = Order.objects.select_related('telegram_user').prefetch_related(
            'order_items__product'
        ).all()

        # Group orders by chat_id
        grouped_orders = {}
        for order in orders:
            chat_id = order.chat_id
            if chat_id not in grouped_orders:
                grouped_orders[chat_id] = []

            # Convert datetime fields to ISO format
            def datetime_to_str(dt):
                if dt:
                    return dt.isoformat()
                return None

            # Generate order item summaries
            items_summary = []
            for item in order.order_items.all():
                items_summary.append({
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                    'total_sum': item.total_sum
                })

            # Create order summary
            summary = {
                'order_id': order.id,
                'name': order.name,
                'surname': order.surname,
                'phone': order.phone,
                'email': order.email,
                'address': order.address,
                'receiver': order.receiver,
                'receiver_comments': order.receiver_comments,
                'submitted_at': datetime_to_str(order.submitted_at),
                'created_at': datetime_to_str(order.created_at),
                'processed_at': datetime_to_str(order.processed_at),
                'complete_at': datetime_to_str(order.complete_at),
                'canceled_at': datetime_to_str(order.canceled_at),
                'status': order.status,
                'order_items': items_summary
            }

            grouped_orders[chat_id].append(summary)

        # Update OrderSummary
        for chat_id, orders_summary in grouped_orders.items():
            OrderSummary.objects.update_or_create(
                chat_id=chat_id,
                defaults={'orders': orders_summary}
            )
            logger.info(f'Order summaries created/updated for chat ID {chat_id}')
