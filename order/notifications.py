from django.utils import timezone
from django.conf import settings
from .models import Order
import logging
import logging, requests, json
from .shared_utils import get_random_saying
from .signals import update_order_summary

logger = logging.getLogger(__name__)

STATUS_EMOJIS = {
    'en': {
        'submitted': '📝',
        'created': '🆕',
        'processed': '🔄',
        'complete': '✅',
        'canceled': '❌'
    },
    'uk': {
        'submitted': '📝',
        'created': '🆕',
        'processed': '🔄',
        'complete': '✅',
        'canceled': '❌'
    }
}

MESSAGES = {
    'en': {
        'submitted': "You have a new order #{order_id}. Status of order: {emoji} {status}.",
        'status_changed': "Status of order #{order_id} has been changed to {emoji} {status}.",
        'order_details': "Order Details:\n{order_items_en}",
        'random_saying': "💬 {saying}",
    },
    'uk': {
        'submitted': "У вас нове замовлення #{order_id}. Статус замовлення: {emoji} {status}.",
        'status_changed': "Статус замовлення #{order_id} змінено на {emoji} {status}.",
        'order_details': "Деталі замовлення:\n{order_items_uk}",
        'random_saying': "💬 {saying}",
    }
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

def update_order_status_with_notification(order_id, order_items, new_status, status_field, chat_id, language):
    try:
        order = Order.objects.get(id=order_id)
        setattr(order, status_field, timezone.now())
        order.status = new_status
        order.save()
        order.language = language

        emoji = STATUS_EMOJIS[language].get(new_status, '')
        status_translation = new_status.capitalize() if language == 'en' else {
            'submitted': 'Подано',
            'created': 'Створено',
            'processed': 'Оброблено',
            'complete': 'Завершено',
            'canceled': 'Скасовано'
        }.get(new_status, '')

        # Prepare order details for the message
        order_items_details = "\n".join([
            f"{item.product.name_uk if language == 'uk' else item.product.name_en} - {item.quantity} x {item.product.price} {item.product.currency}" 
            for item in order_items
        ])

        if new_status == 'submitted':
            message = (
                f"\n<a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a>. "
                f"{MESSAGES[language]['submitted'].format(order_id=order_id, emoji=emoji, status=status_translation)}\n"
                f"{MESSAGES[language]['order_details'].replace('{order_items_uk}', '{order_items_en}' if language == 'en' else '{order_items_uk}').format(order_items_en=order_items_details, order_items_uk=order_items_details)}\n\n"
                f"<i>{MESSAGES[language]['random_saying'].format(saying=get_random_saying(settings.SAYINGS_FILE_PATH))}</i>\n"
            )
        else:
            message = (
                f"\n<a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a>. "
                f"{MESSAGES[language]['status_changed'].format(order_id=order_id, emoji=emoji, status=status_translation)}\n"
                f"{MESSAGES[language]['order_details'].replace('{order_items_uk}', '{order_items_en}' if language == 'en' else '{order_items_uk}').format(order_items_en=order_items_details, order_items_uk=order_items_details)}\n\n"
                f"<i>{MESSAGES[language]['random_saying'].format(saying=get_random_saying(settings.SAYINGS_FILE_PATH))}</i>\n"
            )
        send_telegram_message(chat_id, message)
        update_order_summary()

    except Order.DoesNotExist:
        logger.error(f"Order with id {order_id} does not exist.")
    except Exception as e:
        logger.error(f"Error updating order status or sending notification: {e}")
