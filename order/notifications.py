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
        setattr(order, status_field, timezone.now())  # Update status timestamp
        order.status = new_status
        order.save()

        status = new_status.capitalize()
        emoji = STATUS_EMOJIS.get(new_status, '')

        # Prepare order items details
        order_items_details = "\n".join([
            f"{item.product.name} - {item.quantity} x {item.product.price} {item.product.currency}" 
            for item in order_items
        ])

        # Create the message based on the status change
        if new_status == 'submitted':
            message = (
                f"\n"
                f"<a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a>. You have a new order #{order_id}. Status of order: {emoji} {status}. \n"
                f"Order Details:\n{order_items_details}\n\n"
                f"<i>💬 {get_random_saying(settings.SAYINGS_FILE_PATH)}</i>\n"
            )
        else:
            message = (
                f"\n"
                f"<a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a>. Status of order #{order_id} has been changed to {emoji} {status}. \n"
                f"Order Details:\n{order_items_details}\n\n"
                f"<i>💬 {get_random_saying(settings.SAYINGS_FILE_PATH)}</i>\n"
            )

        # Send the message via Telegram
        send_telegram_message(chat_id, message)

        # Update the order summary with the desired structure
        update_order_summary_for_chat_id(chat_id, order)

    except Order.DoesNotExist:
        logger.error(f"Order with id {order_id} does not exist.")
    except Exception as e:
        logger.error(f"Error updating order status or sending notification: {e}")


def datetime_to_str(dt):
    """Convert datetime to string format 'YYYY-MM-DD HH:MM'."""
    return dt.strftime('%Y-%m-%d %H:%M') if dt else None


def update_order_summary_for_chat_id(chat_id, order):
    try:
        # Retrieve all orders by the phone associated with this order
        orders = Order.objects.filter(phone=order.phone)

        # Construct order summary with the expected format
        summary = []
        for order in orders:
            # Serialize order items with detailed fields
            order_items = [{
                'product_name': item.product.name,
                'collection_name': item.product.collection.name,
                'size': item.size,
                'color_name': item.color.name,
                'color_value': item.color.value,
                'quantity': item.quantity,
                'total_sum': item.quantity * item.price,
                'item_price': f'{item.price:.2f}'
            } for item in order.order_items.all()]

            # Add order data to summary
            summary.append({
                'order_id': order.id,
                'created_at': datetime_to_str(order.created_at),
                'submitted_at': datetime_to_str(order.submitted_at),
                'processed_at': datetime_to_str(order.processed_at),
                'complete_at': datetime_to_str(order.complete_at),
                'canceled_at': datetime_to_str(order.canceled_at),
                'order_items': order_items
            })

        # Update or create an OrderSummary for the given chat_id
        OrderSummary.objects.update_or_create(
            chat_id=chat_id,
            defaults={'orders': summary}
        )
        logger.info(f'Order summary updated for chat ID {chat_id}')
    
    except Exception as e:
        logger.error(f'Error updating order summary for chat ID {chat_id}: {e}')
