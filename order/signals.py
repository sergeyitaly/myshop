import os
import random
import requests
import logging
from django.utils import timezone
from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import is_aware, make_naive
from django.utils.dateparse import parse_datetime

from .models import Order, OrderSummary, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

logger = logging.getLogger(__name__)
STATUS_EMOJIS = {
    'submitted': '📝',
    'created': '🆕',
    'processed': '🔄',
    'complete': '✅',
    'canceled': '❌'
}

def ensure_datetime(value):
    if isinstance(value, str):
        value = parse_datetime(value)
    return value

def datetime_to_str(dt):
    if isinstance(dt, str):
        dt = parse_datetime(dt)
    if dt:
        if is_aware(dt):
            dt = make_naive(dt)
        return dt.strftime('%Y-%m-%d %H:%M')
    return None

def safe_make_naive(dt):
    dt = ensure_datetime(dt)
    if dt is None:
        return None
    return make_naive(dt) if is_aware(dt) else dt

def get_order_summary(order):
    submitted_at = safe_make_naive(order.submitted_at)
    last_status_time = safe_make_naive(
        order.canceled_at or order.complete_at or order.processed_at or order.created_at or order.submitted_at
    )

    order_items_data = OrderItemSerializer(order.order_items.all(), many=True).data

    summary = {
        'order_id': order.id,
        'order_items': order_items_data,
        'last_status': order.status,
        'last_status_time': datetime_to_str(last_status_time),
        'submitted_at': datetime_to_str(submitted_at)
    }
    return summary

def get_chat_id_from_phone(phone_number):
    try:
        response = requests.get(f'{settings.VERCEL_DOMAIN}/api/telegram_user', params={'phone': phone_number})
        response.raise_for_status()
        data = response.json()
        
        if 'chat_id' in data:
            return data['chat_id']
        else:
            logger.error(f"No chat_id found for phone number: {phone_number}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to /api/telegram_user failed: {e}")
        return None

def update_order_summary_for_phone(phone_number):
    chat_id = get_chat_id_from_phone(phone_number)
    if chat_id:
        update_order_summary_for_chat_id(chat_id)
    else:
        logger.error(f"Failed to update order summary for phone number: {phone_number}")

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


def get_random_saying(file_path):
    if not os.path.exists(file_path):
        logger.error(f"Failed to read sayings file: [Errno 2] No such file or directory: '{file_path}'")
        return "No sayings available."
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sayings = [line.strip() for line in file if line.strip()]
        
        if not sayings:
            logger.error("Sayings file is empty.")
            return "No sayings available."
        
        return random.choice(sayings)
    except Exception as e:
        logger.error(f"Error reading sayings file: {e}")
        return "No sayings available."

def update_order_status_with_notification(order_id, new_status, status_field, chat_id):
    try:
        order = Order.objects.get(id=order_id)
        setattr(order, status_field, timezone.now())
        order.status = new_status
        order.save()

        status = new_status.capitalize()
        emoji = STATUS_EMOJIS.get(new_status, '')
        message = (f"<a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a>.\n"
                   f"Status of order #{order_id} has been changed to {emoji} {status}. \n\n"
                   f"<i>💬 {get_random_saying(settings.SAYINGS_FILE_PATH)}</i>")
        
        send_telegram_message(chat_id, message)
        update_order_summary_for_chat_id(chat_id)
    except Order.DoesNotExist:
        logger.error(f"Order with id {order_id} does not exist.")

@receiver(post_save, sender=Order)
def update_order_summary(sender, instance, created, **kwargs):
    if created:
        phone_number = instance.phone
        if phone_number:
            chat_id = get_chat_id_from_phone(phone_number)
            if chat_id:
                update_order_status_with_notification(
                    instance.id,
                    instance.status,
                    f'{instance.status}_at',
                    chat_id
                )
            else:
                logger.error(f"No chat_id found for phone number: {phone_number}")
    else:
        # Handle status changes if needed
        pass

@receiver(post_save, sender=OrderItem)
def update_order_summary_on_order_item_change(sender, instance, **kwargs):
    order = instance.order
    phone_number = order.phone  # Make sure this field matches your model
    if phone_number:
        chat_id = get_chat_id_from_phone(phone_number)
        if chat_id:
            logger.debug(f"OrderItem change detected for Order ID: {order.id}, updating summary for chat_id: {chat_id}")
            update_order_summary_for_chat_id(chat_id)

@receiver(post_delete, sender=Order)
def remove_order_from_summary(sender, instance, **kwargs):
    phone_number = instance.phone  # Make sure this field matches your model
    if phone_number:
        chat_id = get_chat_id_from_phone(phone_number)
        if chat_id:
            try:
                logger.debug(f"Removing Order ID: {instance.id} from summary for chat_id: {chat_id}")

                order_summary = OrderSummary.objects.get(chat_id=chat_id)
                order_summary.orders = [order for order in order_summary.orders if order['order_id'] != instance.id]
                order_summary.save()
                
                cache_key = f'order_summary_{chat_id}'
                cache.delete(cache_key)
            except OrderSummary.DoesNotExist:
                pass

@receiver(post_delete, sender=OrderItem)
def update_order_summary_on_order_item_delete(sender, instance, **kwargs):
    order = instance.order
    phone_number = order.phone  # Make sure this field matches your model
    if phone_number:
        chat_id = get_chat_id_from_phone(phone_number)
        if chat_id:
            update_order_summary_for_chat_id(chat_id)

            logger.debug(f"OrderItem deleted for Order ID: {order.id}, updating summary for chat_id: {chat_id}")
