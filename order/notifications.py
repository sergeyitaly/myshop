# notifications.py
from django.utils import timezone
from django.conf import settings
from .models import Order
from .shared_utils import get_random_saying
import logging
import requests
from django.core.cache import cache
from .models import Order, OrderSummary
from .serializers import OrderItemSerializer
from datetime import datetime
from .shared_utils import get_random_saying
from django.utils.timezone import is_aware, make_naive
from django.dispatch import receiver
from django.db.models.signals import post_save

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
        update_order_summary_for_chat_id(chat_id, order)
    except Order.DoesNotExist:
        logger.error(f"Order with id {order_id} does not exist.")
    except Exception as e:
        logger.error(f"Error updating order status or sending notification: {e}")


def safe_make_naive(dt):
    """Safely convert an aware datetime to naive."""
    if dt is None:
        return None
    return make_naive(dt) if is_aware(dt) else dt

def datetime_to_str(dt):
    """Convert datetime to string format."""
    return dt.strftime('%Y-%m-%d %H:%M') if dt else None


def update_order_summary_for_chat_id(chat_id, order):
    try:
        # Filter orders based on the chat_id
        orders = Order.objects.filter(phone=order.phone)

        # Create a list of order summaries
        summary = []
        for order in orders:
            serializer = OrderItemSerializer(order.order_items.all(), many=True)
            order_data = serializer.data
            summary.append({
                'order_id': order.id,
                'order_items': order_data,
                'submitted_at': order.submitted_at.strftime('%Y-%m-%d %H:%M') if order.submitted_at else None,
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M') if order.created_at else None,
                'processed_at': order.processed_at.strftime('%Y-%m-%d %H:%M') if order.processed_at else None,
                'complete_at': order.complete_at.strftime('%Y-%m-%d %H:%M') if order.complete_at else None,
                'canceled_at': order.canceled_at.strftime('%Y-%m-%d %H:%M') if order.canceled_at else None,
            })

        # Update or create the OrderSummary instance
        OrderSummary.objects.update_or_create(
            chat_id=chat_id,
            defaults={'orders': summary}
        )
        logger.info(f'Order summary updated for chat ID {chat_id}')
    
    except Exception as e:
        logger.error(f'Error updating order summary for chat ID {chat_id}: {e}')
