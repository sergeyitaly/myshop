import os
import random
import requests
import logging

from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import is_aware, make_naive
from django.utils.dateparse import parse_datetime

from .models import Order, OrderSummary, OrderItem
from .serializers import OrderItemSerializer

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
    dt = ensure_datetime(dt)
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
    created_at = safe_make_naive(order.created_at)
    processed_at = safe_make_naive(order.processed_at)
    complete_at = safe_make_naive(order.complete_at)
    canceled_at = safe_make_naive(order.canceled_at)

    order_items_data = OrderItemSerializer(order.order_items.all(), many=True).data

    summary = {
        'order_id': order.id,
        'submitted_at': datetime_to_str(submitted_at),
        'created_at': datetime_to_str(created_at),
        'processed_at': datetime_to_str(processed_at),
        'complete_at': datetime_to_str(complete_at),
        'canceled_at': datetime_to_str(canceled_at),
        'order_items': order_items_data
    }
    return summary

def update_order_summary_for_chat_id(chat_id):
    logger.debug(f"Updating order summary for chat_id: {chat_id}")
    
    if chat_id:
        # Get or create the OrderSummary object
        order_summary, created = OrderSummary.objects.get_or_create(chat_id=chat_id)
        logger.debug(f"OrderSummary created: {created}")

        # Fetch all orders for the given chat_id
        orders = Order.objects.filter(telegram_user__chat_id=chat_id)
        
        # Update the summary with current details and statuses of all orders
        order_summaries = [get_order_summary(order) for order in orders]
        
        # Update or create summary of each order
        order_summary.orders = order_summaries
        order_summary.save()

        # Cache the updated order summary
        cache_key = f'order_summary_{chat_id}'
        cache.set(cache_key, order_summary, timeout=60 * 15)
        logger.debug(f"OrderSummary saved and cached: {order_summary}")


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
        setattr(order, status_field, new_status)
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
def update_order_summary(sender, instance, **kwargs):
    chat_id = instance.telegram_user.chat_id if instance.telegram_user else None
    update_order_summary_for_chat_id(chat_id)

    if kwargs.get('submitted', False):
        message = (f"<b>Вітаємо!</b>\n\n"
                   f"Ви створили нове замовлення № <b>{instance.id}</b> на сайті "
                   f"<a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a>.\n"
                   f"Деталі замовлення відправлено на email {instance.email}.\n\n"
                   f"<i>💬 {get_random_saying(settings.SAYINGS_FILE_PATH)}</i>\n\n"
                   f"<b>Дякуємо, що обрали нас!</b> 🌟")
        send_telegram_message(chat_id, message)
    else:
        status = instance.status.capitalize()
        emoji = STATUS_EMOJIS.get(instance.status, '')
        message = (f"<a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a>.\n"
                   f"Status of order #{instance.id} has been changed to {emoji} {status}. \n\n"
                   f"<i>💬 {get_random_saying(settings.SAYINGS_FILE_PATH)}</i>")
        send_telegram_message(chat_id, message)

@receiver(post_save, sender=OrderItem)
def update_order_summary_on_order_item_change(sender, instance, **kwargs):
    order = instance.order
    chat_id = order.telegram_user.chat_id if order.telegram_user else None
    update_order_summary_for_chat_id(chat_id)

@receiver(post_delete, sender=Order)
def remove_order_from_summary(sender, instance, **kwargs):
    chat_id = instance.telegram_user.chat_id if instance.telegram_user else None
    if chat_id:
        try:
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
    chat_id = order.telegram_user.chat_id if order.telegram_user else None
    update_order_summary_for_chat_id(chat_id)
