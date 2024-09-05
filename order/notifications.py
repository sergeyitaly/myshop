# notifications.py
from django.utils import timezone
from django.conf import settings
from .models import Order
from .shared_utils import get_random_saying
import logging
import requests
from django.core.cache import cache
from .models import Order, OrderSummary
from .serializers import OrderSerializer
from datetime import datetime
from .shared_utils import get_random_saying
from django.utils.timezone import is_aware, make_naive

logger = logging.getLogger(__name__)

STATUS_EMOJIS = {
    'submitted': '📝',
    'created': '🆕',
    'processed': '🔄',
    'complete': '✅',
    'canceled': '❌'
}

def send_telegram_message(chat_id, message):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        result = response.json()
        if not result.get('ok'):
            logger.error(f"Telegram API returned an error: {result.get('description')}")
        else:
            logger.info(f"Telegram message sent successfully: {result}")
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to Telegram API failed: {e}")
        raise

def update_order_status_with_notification(order_id, order_items, new_status, status_field, chat_id):
    try:
        order = Order.objects.get(id=order_id)
        setattr(order, status_field, timezone.now())
        order.status = new_status
        order.save()

        status = new_status.capitalize()
        emoji = STATUS_EMOJIS.get(new_status, '')

        order_items_details = "\n".join([
            f"{item.product.name} - {item.quantity} x {item.product.price} {item.product.currency}" 
            for item in order_items
        ])

        if new_status == 'submitted':       
            message = (
                f"\n"
                f"<a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a>. You have a new order #{order_id}. Status of order:  {emoji} {status}. \n"
                f"Order Details:\n{order_items_details}\n\n"
                f"<i>💬 {get_random_saying(settings.SAYINGS_FILE_PATH)}</i> \n"
            )
        else:
            message = (
                f"\n"
                f"<a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a>. Status of order #{order_id} has been changed to {emoji} {status}. \n"
                f"Order Details:\n{order_items_details}\n\n"
                f"<i>💬 {get_random_saying(settings.SAYINGS_FILE_PATH)}</i> \n"
            )

        send_telegram_message(chat_id, message)
        update_order_summary_for_chat_id(chat_id)
    except Order.DoesNotExist:
        logger.error(f"Order with id {order_id} does not exist.")
    except Exception as e:
        logger.error(f"Error updating order status or sending notification: {e}")

def update_order_summary_for_chat_id(chat_id):
    try:
        # Fetch all orders with related order items and products
        orders = Order.objects.prefetch_related('order_items__product').all()
        # Group orders by chat_id
        grouped_orders = {}
        for order in orders:
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

            # Use the serializer to format the order and items
            serializer = OrderSerializer(order)
            order_data = serializer.data
            # Create order summary with only the required statuses
            summary = {
                'order_id': order.id,
                'order_items': order_data['order_items'],
                'submitted_at': datetime_to_str(submitted_at),
                latest_status_field: datetime_to_str(latest_status_timestamp)
            }
            grouped_orders[chat_id].append(summary)

        # Update OrderSummary
        all_chat_ids = grouped_orders.keys()
        for chat_id in all_chat_ids:
            orders_summary = grouped_orders.get(chat_id, [])
            OrderSummary.objects.update_or_create(
                chat_id=chat_id,
                defaults={'orders': orders_summary}
            )
    except Exception as e:
        logger.error(f'Error while generating order summaries: {e}')