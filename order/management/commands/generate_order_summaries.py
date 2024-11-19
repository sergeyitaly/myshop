from django.utils.translation import gettext as _
from order.models import Product, Order, TelegramUser
from django.core.management.base import BaseCommand
from order.models import OrderSummary
from order.serializers import OrderSerializer
from django.utils.timezone import make_naive, is_aware
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Generate order summaries for previously created orders and update telegram_user_id'

    def handle(self, *args, **kwargs):
        try:
            # Fetch all orders with related order items and products
            orders = Order.objects.prefetch_related('order_items__product').all()

            logger.info(f'Fetched {orders.count()} orders.')

            # Group orders by chat_id
            grouped_orders = {}

            for order in orders:
                # Fetch or update the TelegramUser by phone number
                if not order.telegram_user:
                    try:
                        # Look up the TelegramUser by the phone number
                        telegram_user = TelegramUser.objects.get(phone=order.phone)
                        order.telegram_user = telegram_user
                        order.save()  # Save the updated order with the telegram_user_id
                        logger.info(f'Updated order {order.id} with telegram_user_id {telegram_user.id}')
                    except TelegramUser.DoesNotExist:
                        logger.warning(f'TelegramUser not found for phone {order.phone} (Order ID: {order.id})')
                
                chat_id = order.telegram_user.chat_id if order.telegram_user else None
                if chat_id not in grouped_orders:
                    grouped_orders[chat_id] = []

                # Function to safely convert datetime to naive
                def safe_make_naive(dt):
                    if dt is None:
                        return None
                    return make_naive(dt) if is_aware(dt) else dt

                # Extract and format datetime fields
                submitted_at = safe_make_naive(order.submitted_at)
                created_at = safe_make_naive(order.created_at)
                processed_at = safe_make_naive(order.processed_at)
                complete_at = safe_make_naive(order.complete_at)
                canceled_at = safe_make_naive(order.canceled_at)

                # Determine the latest timestamp directly using datetime
                statuses = {
                    'submitted_at': submitted_at,
                    'created_at': created_at,
                    'processed_at': processed_at,
                    'complete_at': complete_at,
                    'canceled_at': canceled_at
                }

                latest_status_field = max(
                    statuses,
                    key=lambda s: statuses[s] or datetime.min
                )
                latest_status_timestamp = statuses[latest_status_field]

                # Convert datetime to string for summary
                def datetime_to_str(dt):
                    if dt:
                        return dt.strftime('%Y-%m-%d %H:%M')
                    return None

                # Create the order items in both English and Ukrainian
                order_items_en = []
                order_items_uk = []
                for item in order.order_items.all():  # Fetch the actual OrderItem objects
                    product = item.product  # Get the actual Product instance

                    # Directly access translated fields for English and Ukrainian
                    product_name_en = product.name_en  # Access translated 'name' field for current language
                    product_name_uk = product.name_uk  # Access translated 'name_uk' field
                    color_name_en = product.color_name_en  # Assuming 'color_name' field is translated
                    color_name_uk = product.color_name_uk  # Assuming 'color_name_uk' exists
                    size = product.size  # Assuming 'size' field is translated

                    # English order item
                    order_items_en.append({
                        'size': size,
                        'quantity': item.quantity,
                        'color_name': color_name_en,
                        'price': product.price,  # Assuming 'price' field exists in Product
                        'color_value': product.color_value,  # Assuming 'color_value' exists in Product
                        'name': product_name_en,
                        'collection_name': product.collection.name_en if product.collection else _('No Collection')  # Assuming related 'collection'
                    })

                    # Ukrainian order item (using translation)
                    order_items_uk.append({
                        'size': size,
                        'quantity': item.quantity,
                        'color_name': color_name_uk,
                        'price': product.price,  # Assuming 'price' field exists and is the same for both languages
                        'color_value': product.color_value,  # Assuming 'color_value' exists for both languages
                        'name': product_name_uk,
                        'collection_name': product.collection.name_uk if product.collection else _('No Collection')  # Assuming related 'collection' in Ukrainian
                    })

                # Create order summary with both English and Ukrainian order items
                summary = {
                    'order_id': order.id,
                    'order_items_en': order_items_en,
                    'order_items_uk': order_items_uk,
                    'submitted_at': datetime_to_str(submitted_at),
                    latest_status_field: datetime_to_str(latest_status_timestamp)
                }

                grouped_orders[chat_id].append(summary)

            # Log grouped orders for debugging
            logger.info(f'Grouped Orders: {grouped_orders}')

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
