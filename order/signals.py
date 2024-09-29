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
    return make_naive(dt) if dt and is_aware(dt) else dt

def get_chat_id_from_phone(phone_number):
    try:
        response = requests.get(f'{settings.VERCEL_DOMAIN}/api/telegram_user', params={'phone': phone_number})
        response.raise_for_status()
        return response.json().get('chat_id')
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get chat_id from /api/telegram_user: {e}")
        return None

def build_order_summary(order):
    submitted_at = safe_make_naive(order.submitted_at)
    latest_status = safe_make_naive(order.canceled_at or order.complete_at or order.processed_at or order.created_at or order.submitted_at)
    order_items_data = OrderItemSerializer(order.order_items.all(), many=True).data

    return {
        'order_id': order.id,
        'order_items': [{
            'size': item['size'],
            'quantity': item['quantity'],
            'total_sum': item['total_sum'],
            'color_name': item['color_name'],
            'item_price': item['item_price'],
            'color_value': item['color_value'],
            'product_name': item['product_name'],
            'collection_name': item['collection_name']
        } for item in order_items_data],
        'processed_at': datetime_to_str(latest_status),
        'submitted_at': datetime_to_str(submitted_at)
    }

def update_order_summary_for_chat(chat_id):
    try:
        orders = Order.objects.filter(telegram_user__chat_id=chat_id).prefetch_related('order_items__product')
        order_summaries = [build_order_summary(order) for order in orders]
        
        OrderSummary.objects.update_or_create(
            chat_id=chat_id,
            defaults={'orders': order_summaries}
        )
        logger.info(f"Order summaries updated for chat ID {chat_id}")
    except Exception as e:
        logger.error(f"Error updating order summaries for chat ID {chat_id}: {e}")

@receiver(post_save, sender=Order)
@receiver(post_save, sender=OrderItem)
def update_order_summary_on_save(sender, instance, **kwargs):
    order = instance if isinstance(instance, Order) else instance.order
    if order.phone:
        chat_id = get_chat_id_from_phone(order.phone)
        if chat_id:
            update_order_summary_for_chat(chat_id)
        else:
            logger.error(f"No chat_id found for phone number: {order.phone}")
    else:
        logger.error(f"Order ID {order.id} has no associated phone number.")

@receiver(post_delete, sender=Order)
@receiver(post_delete, sender=OrderItem)
def remove_order_from_summary(sender, instance, **kwargs):
    order = instance if isinstance(instance, Order) else instance.order
    if order.phone:
        chat_id = get_chat_id_from_phone(order.phone)
        if chat_id:
            try:
                order_summary = OrderSummary.objects.get(chat_id=chat_id)
                order_summary.orders = [o for o in order_summary.orders if o['order_id'] != order.id]
                order_summary.save()
                cache.delete(f'order_summary_{chat_id}')
                logger.info(f"Order ID {order.id} removed from chat ID {chat_id}'s summary.")
            except OrderSummary.DoesNotExist:
                logger.warning(f"OrderSummary not found for chat ID {chat_id}.")
            except Exception as e:
                logger.error(f"Error removing order ID {order.id} from summary: {e}")
