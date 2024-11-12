from django.utils import timezone
from django.conf import settings
from .models import Order
import logging
import requests
from django.utils.translation import gettext as _  # Import gettext for translation
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

        # Determine the language from the `order_items` (assuming you have language fields like `product_name_en` and `product_name_uk`)
        # Here, we will just check the first item to get the language preference, assuming it's consistent across all items
        language = 'en'  # Default to English if no language field found
        if order_items:
            # Check the first order item for the language
            first_item = order_items[0]
            if first_item.product_name_uk:  # Assuming 'product_name_uk' exists in your model
                language = 'uk'  # If Ukrainian name exists, use Ukrainian language
            
        # Adjusting the order items details based on the detected language
        order_items_details = "\n".join([
            f"{item.product.product_name_en} - {item.quantity} x {item.product.price} {item.product.currency}" 
            if language == 'en' else
            f"{item.product.product_name_uk} - {item.quantity} x {item.product.price} {item.product.currency}" 
            for item in order_items
        ])

        if new_status == 'submitted':
            message = (
                f"\n"
                f"<a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a>. {_(f'You have a new order #{order_id}. Status of order:')} {emoji} {status}. \n"
                f"{_(f'Order Details:')}\n{order_items_details}\n\n"
                f"<i>💬 {get_random_saying(settings.SAYINGS_FILE_PATH)}</i> \n"
            )
        else:
            message = (
                f"\n"
                f"<a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a>. {_(f'Status of order #{order_id} has been changed to')} {emoji} {status}. \n"
                f"{_(f'Order Details:')}\n{order_items_details}\n\n"
                f"<i>💬 {get_random_saying(settings.SAYINGS_FILE_PATH)}</i> \n"
            )

        send_telegram_message(chat_id, message)
        update_order_summary(chat_id)

    except Order.DoesNotExist:
        logger.error(f"Order with id {order_id} does not exist.")
    except Exception as e:
        logger.error(f"Error updating order status or sending notification: {e}")
