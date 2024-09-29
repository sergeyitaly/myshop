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
from .serializers import OrderItemSerializer, OrderSerializer

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
        'order_items': [
            {
                'size': item['size'],
                'quantity': item['quantity'],
                'total_sum': item['total_sum'],
                'color_name': item['color_name'],
                'item_price': item['item_price'],
                'color_value': item['color_value'],
                'product_name': item['product_name'],
                'collection_name': item['collection_name']
            } for item in order_items_data
        ],
        'processed_at': datetime_to_str(last_status_time),  # Keep only the most recent status time
        'submitted_at': datetime_to_str(submitted_at)
    }

    return summary

def update_order_summary_for_chat_id():
    try:
        orders = Order.objects.prefetch_related('order_items__product').all()
        logger.info(f'Fetched {orders.count()} orders.')
        grouped_orders = {}
        for order in orders:
            chat_id = order.telegram_user.chat_id if order.telegram_user else None
            if chat_id not in grouped_orders:
                grouped_orders[chat_id] = []
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
            def datetime_to_str(dt):
                if dt:
                    return dt.strftime('%Y-%m-%d %H:%M')
                return None
            summary = {
                'order_id': order.id,
                'order_items': [
                    {
                        'size': item.size,
                        'quantity': item.quantity,
                        'total_sum': item.total_sum,
                        'color_name': item.product.color.name,
                        'item_price': str(item.product.price),
                        'color_value': item.product.color.value,
                        'product_name': item.product.name,
                        'collection_name': item.product.collection.name,
                    } for item in order.order_items.all()
                ],
                'submitted_at': datetime_to_str(submitted_at),
                latest_status_field: datetime_to_str(latest_status_timestamp)
            }
            existing_summary = next((o for o in grouped_orders[chat_id] if o['order_id'] == order.id), None)
            if existing_summary:
                grouped_orders[chat_id].remove(existing_summary)
            
            grouped_orders[chat_id].append(summary)
        logger.info(f'Grouped Orders: {grouped_orders}')
        all_chat_ids = grouped_orders.keys()
        for chat_id in all_chat_ids:
            orders_summary = grouped_orders.get(chat_id, [])
            OrderSummary.objects.update_or_create(
                chat_id=chat_id,
                defaults={'orders': orders_summary}
            )
            logger.info(f'Order summaries created/updated for chat ID {chat_id}')

    except Exception as e:
        logger.error(f'Error while generating order summaries: {e}')

def get_chat_id_from_phone(phone_number):
    try:
        response = requests.get(f'{settings.VERCEL_DOMAIN}/api/telegram_user', params={'phone': phone_number})
        response.raise_for_status()
        data = response.json()
        
        return data.get('chat_id')
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to /api/telegram_user failed: {e}")
        return None

@receiver(post_save, sender=Order)
def update_order_summary(sender, instance, **kwargs):
        phone_number = instance.phone
        if phone_number:
            chat_id = get_chat_id_from_phone(phone_number)
            if chat_id:
                update_order_summary_for_chat_id()
            else:
                logger.error(f"No chat_id found for phone number: {phone_number}")
        else:
            logger.error(f"No phone number found for order ID: {instance.id}")


@receiver(post_save, sender=OrderItem)
def update_order_summary_on_order_item_change(sender, instance, **kwargs):
    order = instance.order
    phone_number = order.phone
    if phone_number:
        chat_id = get_chat_id_from_phone(phone_number)
        if chat_id:
            update_order_summary_for_chat_id()
            logger.debug(f"OrderItem change detected for Order ID: {order.id}, updating summary for chat_id: {chat_id}")

@receiver(post_delete, sender=Order)
def remove_order_from_summary(sender, instance, **kwargs):
    phone_number = instance.phone  # Make sure this field matches your model
    if phone_number:
        chat_id = get_chat_id_from_phone(phone_number)
        if chat_id:
            try:
                logger.debug(f"Removing Order ID: {instance.id} from summary for chat_id: {chat_id}")
                order_summary = OrderSummary.objects.get(chat_id=chat_id)
                updated_orders = [order for order in order_summary.orders if order['order_id'] != instance.id]
                order_summary.orders = updated_orders
                order_summary.save()
                cache_key = f'order_summary_{chat_id}'
                cache.delete(cache_key)

            except OrderSummary.DoesNotExist:
                # Log the exception if needed
                logger.warning(f"OrderSummary with chat_id {chat_id} does not exist")
            except Exception as e:
                # Log any other exceptions
                logger.error(f"Error while removing Order ID: {instance.id} from summary: {str(e)}")

@receiver(post_delete, sender=OrderItem)
def update_order_summary_on_order_item_delete(sender, instance, **kwargs):
    order = instance.order
    phone_number = order.phone  # Make sure this field matches your model
    if phone_number:
        chat_id = get_chat_id_from_phone(phone_number)
        if chat_id:
            update_order_summary_for_chat_id()
            logger.debug(f"OrderItem deleted for Order ID: {order.id}, updating summary for chat_id: {chat_id}")
