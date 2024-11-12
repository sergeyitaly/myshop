from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext as _
from .models import Order
import logging
import requests
from .shared_utils import get_random_saying
from .signals import update_order_summary

logger = logging.getLogger(__name__)

STATUS_EMOJIS = {
    'submitted': '📝',
    'created': '🆕',
    'processed': '🔄',
    'complete': '✅',
    'canceled': '❌'
}

def send_telegram_message(chat_id, message):
    """
    Send a message via Telegram using the bot token and chat ID.
    """
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
    """
    Update the status of an order and send a notification via Telegram.
    """
    try:
        order = Order.objects.get(id=order_id)
        setattr(order, status_field, timezone.now())
        order.status = new_status
        order.save()

        # Determine language for the notification based on the order items
        language = 'en' if not order_items[0].product_name_uk else 'uk'
        
        # Construct the order items list based on the determined language
        order_items_details = "\n".join([
            f"{item.product.product_name_en if language == 'en' else item.product.product_name_uk} - "
            f"{item.quantity} x {item.product.price} {item.product.currency}" 
            for item in order_items
        ])

        # Compose the notification message based on order status
        status = new_status.capitalize()
        emoji = STATUS_EMOJIS.get(new_status, '')

        if new_status == 'submitted':
            message = (
                f"<a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a>. "
                f"{_('You have a new order')} #{order_id}. {_('Order Status:')} {emoji} {status}. \n"
                f"{_('Order Details:')}\n{order_items_details}\n\n"
                f"<i>💬 {get_random_saying(settings.SAYINGS_FILE_PATH)}</i>"
            )
        else:
            message = (
                f"<a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a>. "
                f"{_('Order')} #{order_id} {_('status changed to')} {emoji} {status}. \n"
                f"{_('Order Details:')}\n{order_items_details}\n\n"
                f"<i>💬 {get_random_saying(settings.SAYINGS_FILE_PATH)}</i>"
            )

        # Send the message and update order summary
        send_telegram_message(chat_id, message)
        update_order_summary(chat_id)

    except Order.DoesNotExist:
        logger.error(f"Order with id {order_id} does not exist.")
    except Exception as e:
        logger.error(f"Error updating order status or sending notification: {e}")
