import requests
import logging
from datetime import datetime
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
    """Ensures the value is a datetime object."""
    if isinstance(value, str):
        return parse_datetime(value)
    return value

def datetime_to_str(dt):
    """Converts a datetime object to string, handling naive and aware datetimes."""
    dt = ensure_datetime(dt)
    if dt:
        if is_aware(dt):
            dt = make_naive(dt)
        return dt.strftime('%Y-%m-%d %H:%M')
    return None

def get_order_summary(order):
    """Generates a summary of an order."""
    submitted_at = ensure_datetime(order.submitted_at)
    last_status_time = ensure_datetime(order.canceled_at or order.complete_at or order.processed_at or order.created_at)
    
    order_items_data = OrderItemSerializer(order.order_items.all(), many=True).data
    summary = {
        'order_id': order.id,
        'order_items': [
            {
                'size': item['size'],
                'quantity': item['quantity'],
                'total_sum': item['total_sum'],
                'color_name': item['color_name'],
                'item_price': item['item_price'],
                'color_value': item['color_value'],
                'product_name': item['product_name'],
                'collection_name': item['collection_name'],
            } for item in order_items_data
        ],
        'processed_at': datetime_to_str(last_status_time),
        'submitted_at': datetime_to_str(submitted_at),
    }
    return summary

def update_order_summary():
    """Updates the summary of orders grouped by Telegram chat ID."""
    try:
        orders = Order.objects.prefetch_related('order_items__product').all()
        logger.info(f'Fetched {orders.count()} orders.')
        grouped_orders = {}

        for order in orders:
            order_chat_id = order.telegram_user.chat_id if order.telegram_user else None
            if not order_chat_id:
                continue

            if order_chat_id not in grouped_orders:
                grouped_orders[order_chat_id] = []

            summary = get_order_summary(order)
            existing_summary = next((o for o in grouped_orders[order_chat_id] if o['order_id'] == order.id), None)
            if existing_summary:
                grouped_orders[order_chat_id].remove(existing_summary)
            grouped_orders[order_chat_id].append(summary)

        for chat_id, orders_summary in grouped_orders.items():
            OrderSummary.objects.update_or_create(
                chat_id=chat_id,
                defaults={'orders': orders_summary}
            )
            logger.info(f'Order summaries created/updated for chat ID {chat_id}')

    except Exception as e:
        logger.error(f'Error while generating order summaries: {e}')

def get_chat_id_from_phone(phone_number):
    """Fetches the Telegram chat ID from the user's phone number."""
    try:
        response = requests.get(f'{settings.VERCEL_DOMAIN}/api/telegram_user', params={'phone': phone_number})
        response.raise_for_status()
        return response.json().get('chat_id')
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to /api/telegram_user failed: {e}")
        return None

@receiver(post_save, sender=OrderItem)
def update_order_summary_on_order_item_change(sender, instance, **kwargs):
    """Updates the order summary when an OrderItem is changed."""
    phone_number = instance.order.phone
    if phone_number:
        chat_id = get_chat_id_from_phone(phone_number)
        if chat_id:
            update_order_summary()
            logger.debug(f"OrderItem updated for Order ID: {instance.order.id}, summary updated for chat ID: {chat_id}")

@receiver(post_delete, sender=Order)
def remove_order_from_summary(sender, instance, **kwargs):
    """Removes an order from the summary when an order is deleted."""
    phone_number = instance.phone
    if phone_number:
        chat_id = get_chat_id_from_phone(phone_number)
        if chat_id:
            try:
                order_summary = OrderSummary.objects.get(chat_id=chat_id)
                updated_orders = [o for o in order_summary.orders if o['order_id'] != instance.id]
                order_summary.orders = updated_orders
                order_summary.save()
                cache.delete(f'order_summary_{chat_id}')
                logger.debug(f"Removed order ID {instance.id} from summary for chat ID {chat_id}")
            except OrderSummary.DoesNotExist:
                logger.warning(f"OrderSummary for chat ID {chat_id} does not exist.")
            except Exception as e:
                logger.error(f"Error removing order from summary: {e}")

@receiver(post_delete, sender=OrderItem)
def update_order_summary_on_order_item_delete(sender, instance, **kwargs):
    """Updates the order summary when an OrderItem is deleted."""
    phone_number = instance.order.phone
    if phone_number:
        chat_id = get_chat_id_from_phone(phone_number)
        if chat_id:
            update_order_summary()
            logger.debug(f"OrderItem deleted for Order ID: {instance.order.id}, summary updated for chat ID: {chat_id}")
