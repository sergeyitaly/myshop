import requests
import logging
from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import is_aware, make_aware, make_naive
from django.db import transaction
from django.core.cache import cache
from order.models import Order, OrderSummary, OrderItem
from order.serializers import OrderItemSerializer
from django_redis import get_redis_connection
from celery.signals import task_postrun

@task_postrun.connect
def close_redis_connection(sender=None, **kwargs):
    # Close the Redis connection after each task completes
    redis_conn = get_redis_connection('default')
    redis_conn.close()

logger = logging.getLogger(__name__)

STATUS_EMOJIS = {
    'submitted': '📝',
    'created': '🆕',
    'processed': '🔄',
    'complete': '✅',
    'canceled': '❌'
}

def ensure_datetime(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            logger.error(f"Invalid datetime format: {value}")
            return None
    raise ValueError("Invalid datetime value")

def make_aware_if_naive(dt):
    if dt and not is_aware(dt):
        return make_aware(dt)
    return dt

def safe_make_naive(timestamp):
    if isinstance(timestamp, str):
        try:
            timestamp = datetime.fromisoformat(timestamp)  # Parse string to datetime
        except ValueError:
            logger.error(f"Invalid timestamp format: {timestamp}")
            return None
    if timestamp is not None and is_aware(timestamp):
        return make_naive(timestamp)
    elif timestamp is not None and not is_aware(timestamp):
        return timestamp
    return None


def format_timestamp(timestamp):
    return timestamp.strftime('%Y-%m-%d %H:%M') if timestamp else None

def datetime_to_str(dt):
    dt = ensure_datetime(dt)
    if dt:
        dt = make_aware_if_naive(dt)
        return dt.strftime('%Y-%m-%d %H:%M')
    return None


def get_chat_id_from_phone(phone_number):
    # Check if the chat_id is already cached
    cached_chat_id = cache.get(f'chat_id_{phone_number}')
    if cached_chat_id:
        return cached_chat_id

    try:
        # If not cached, make the request
        response = requests.get(
            f'{settings.VERCEL_DOMAIN}/api/telegram_users/by-phone/',
            params={'phone': phone_number},
            timeout=10
        )
        response.raise_for_status()

        response_data = response.json()
        if 'chat_id' in response_data:
            chat_id = response_data['chat_id']
            # Cache the chat_id for 24 hours (86400 seconds)
            cache.set(f'chat_id_{phone_number}', chat_id, timeout=86400)
            return chat_id
        else:
            logger.error(f"No chat_id found for phone number {phone_number}.")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to /api/telegram_users/by-phone failed: {e}")
        return None

    
def get_order_summary(order):
    try:
        # Serialize order items
        order_items_data = OrderItemSerializer(order.order_items.all(), many=True).data
        order_items_en = []
        order_items_uk = []

        # Safely gather status timestamps
        try:
            statuses = {
                'submitted_at': safe_make_naive(getattr(order, 'submitted_at', None)),
                'created_at': safe_make_naive(getattr(order, 'created_at', None)),
                'processed_at': safe_make_naive(getattr(order, 'processed_at', None)),
                'complete_at': safe_make_naive(getattr(order, 'complete_at', None)),
                'canceled_at': safe_make_naive(getattr(order, 'canceled_at', None)),
            }
        except Exception as e:
            logger.error(f"Error initializing statuses for Order ID {order.id}: {e}")
            statuses = {'submitted_at': None}

        # Determine the latest status field and timestamp
        latest_status_field, latest_status_timestamp = 'submitted_at', statuses.get('submitted_at')
        if statuses:
            latest_status_field = max(
                statuses, key=lambda s: statuses[s] or datetime.min
            )
            latest_status_timestamp = statuses.get(latest_status_field)

        # Process order items for English and Ukrainian views
        for item in order_items_data:
            order_item_common = {
                'size': item.get('size'),
                'quantity': item.get('quantity'),
                'price': item.get('price'),
                'currency': item.get('currency'),
                'color_value': item.get('color_value'),
            }
            order_items_en.append({
                **order_item_common,
                'name': item.get('name_en'),
                'color_name': item.get('color_name_en'),
                'collection_name': item.get('collection_name_en'),
            })
            order_items_uk.append({
                **order_item_common,
                'name': item.get('name_uk'),
                'color_name': item.get('color_name_uk'),
                'collection_name': item.get('collection_name_uk'),
            })

        # Return the summary
        return {
            'order_id': order.id,
            'order_items_en': order_items_en,
            'order_items_uk': order_items_uk,
            'submitted_at': format_timestamp(statuses.get('submitted_at')),
            latest_status_field: format_timestamp(latest_status_timestamp),
        }

    except Exception as e:
        logger.error(f"Error generating order summary for Order ID {order.id}: {e}")
        return {}

@transaction.atomic
def update_order_summary():
    try:
        orders = Order.objects.prefetch_related(
            'order_items__product'
        ).select_related('telegram_user')

        grouped_orders = {}
        for order in orders:
            if not order.telegram_user or not order.telegram_user.chat_id:
                continue
            summary = get_order_summary(order)
            grouped_orders.setdefault(order.telegram_user.chat_id, []).append(summary)

        bulk_update = []
        for chat_id, summaries in grouped_orders.items():
            summary_obj, created = OrderSummary.objects.get_or_create(
                chat_id=chat_id,
                defaults={'orders': summaries}
            )
            if not created:
                summary_obj.orders = summaries
                bulk_update.append(summary_obj)

        if bulk_update:
            OrderSummary.objects.bulk_update(bulk_update, ['orders'])
            logger.info("Order summaries updated successfully.")

    except Exception as e:
        logger.exception("Error updating order summaries: %s", e)

@receiver(post_save, sender=OrderItem)
@receiver(post_save, sender=Order)
def update_summary_on_change(sender, instance, **kwargs):
    phone_number = getattr(instance.order, 'phone', None) if sender == OrderItem else instance.phone
    if phone_number:
        chat_id = get_chat_id_from_phone(phone_number)
        if chat_id:
            update_order_summary()
            logger.debug(f"{sender.__name__} updated for chat ID: {chat_id}")

@receiver(post_delete, sender=Order)
def remove_order_from_summary(sender, instance, **kwargs):
    phone_number = instance.phone
    if phone_number:
        chat_id = get_chat_id_from_phone(phone_number)
        if chat_id:
            try:
                order_summary = OrderSummary.objects.get(chat_id=chat_id)
                order_summary.orders = [o for o in order_summary.orders if o['order_id'] != instance.id]
                order_summary.save()
                cache.delete(f'order_summary_{chat_id}')
                update_order_summary()

                logger.info(f"Order ID {instance.id} removed from summary for chat ID {chat_id}")
            except OrderSummary.DoesNotExist:
                logger.warning(f"No summary found for chat ID {chat_id}")
