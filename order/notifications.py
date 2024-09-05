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
        update_order_summary_for_chat_id(chat_id)
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

@receiver(post_save, sender=Order)
def update_order_summary_for_chat_id(order):
    try:
        chat_id = order.telegram_user.chat_id if order.telegram_user else None
        if not chat_id:
            logger.warning(f'Order {order.id} has no associated chat ID.')
            return

        # Extract and format status fields
        statuses = {
            'submitted_at': safe_make_naive(order.submitted_at),
            'created_at': safe_make_naive(order.created_at),
            'processed_at': safe_make_naive(order.processed_at),
            'complete_at': safe_make_naive(order.complete_at),
            'canceled_at': safe_make_naive(order.canceled_at),
        }
        latest_status_field = max(statuses, key=lambda s: statuses[s] or datetime.min)
        latest_status_timestamp = statuses[latest_status_field]

        # Serialize order data
        order_data = OrderSerializer(order).data

        # Prepare order summary data
        summary = {
            'order_id': order.id,
            'order_items': order_data['order_items'],
            'submitted_at': datetime_to_str(statuses['submitted_at']),
            latest_status_field: datetime_to_str(latest_status_timestamp)
        }

        # Get or create OrderSummary for the chat_id
        order_summary, _ = OrderSummary.objects.get_or_create(chat_id=chat_id)

        # Update existing order summaries or add a new one
        existing_orders = order_summary.orders or []
        updated = False

        for i, existing_order in enumerate(existing_orders):
            if existing_order['order_id'] == order.id:
                existing_orders[i] = summary  # Update existing order summary
                updated = True
                break

        if not updated:
            existing_orders.append(summary)  # Add new order summary

        # Save updated order summary
        order_summary.orders = existing_orders
        order_summary.save()
        logger.info(f'Order summary for chat ID {chat_id} updated.')

    except Exception as e:
        logger.error(f"Error updating order summary for chat_id {chat_id}: {e}")
