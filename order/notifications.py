# notifications.py
from django.utils import timezone
from django.conf import settings
from .models import Order
from .shared_utils import safe_make_naive, datetime_to_str, get_random_saying
import logging
import requests
from django.core.cache import cache
from .models import Order, OrderSummary
from .serializers import OrderSerializer
from datetime import datetime

logger = logging.getLogger(__name__)

STATUS_EMOJIS = {
    'submitted': '✅',
    'created': '🛠️',
    'processed': '📦',
    'complete': '🎉',
    'canceled': '❌',
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
    if not chat_id:
        logger.error("Chat ID is missing. Cannot update order summary.")
        return

    logger.debug(f"Updating order summary for chat_id: {chat_id}")

    try:
        order_summary, created = OrderSummary.objects.get_or_create(chat_id=chat_id)
        logger.debug(f"OrderSummary created: {created}")

        orders = Order.objects.filter(telegram_user__chat_id=chat_id).prefetch_related('order_items__product')

        if not orders.exists():
            logger.error(f"No orders found for chat_id: {chat_id}")
            return

        grouped_orders = []
        for order in orders:
            if not order.telegram_user:
                logger.error(f"TelegramUser for Order ID {order.id} not found. Skipping.")
                continue

            submitted_at = safe_make_naive(order.submitted_at)
            created_at = safe_make_naive(order.created_at)
            processed_at = safe_make_naive(order.processed_at)
            complete_at = safe_make_naive(order.complete_at)
            canceled_at = safe_make_naive(order.canceled_at)

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

            serializer = OrderSerializer(order)
            order_data = serializer.data

            logger.info(f'Order {order.id} has {len(order_data["order_items"])} items.')

            summary = {
                'order_id': order.id,
                'order_items': order_data['order_items'],
                latest_status_field: datetime_to_str(latest_status_timestamp),
                'submitted_at': datetime_to_str(submitted_at)
            }

            grouped_orders.append(summary)

        # Update OrderSummary
        order_summary.orders = grouped_orders
        order_summary.save()

        cache_key = f'order_summary_{chat_id}'
        cache.set(cache_key, order_summary, timeout=60 * 15)
        logger.debug(f"OrderSummary saved and cached: {order_summary}")

    except Exception as e:
        logger.error(f"Error updating OrderSummary for chat_id {chat_id}: {e}")
