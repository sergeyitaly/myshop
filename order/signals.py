import requests
import logging
from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import is_aware, make_aware
from django.db import transaction
from django.core.cache import cache
from order.models import Order, OrderSummary, OrderItem
from order.serializers import OrderItemSerializer

logger = logging.getLogger(__name__)

STATUS_EMOJIS = {
    'submitted': '📝',
    'created': '🆕',
    'processed': '🔄',
    'complete': '✅',
    'canceled': '❌',
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

def datetime_to_str(dt):
    dt = ensure_datetime(dt)
    if dt:
        dt = make_aware_if_naive(dt)
        return dt.strftime('%Y-%m-%d %H:%M')
    return None

def get_chat_id_from_phone(phone_number):
    try:
        response = requests.get(
            f'{settings.VERCEL_DOMAIN}/api/telegram_user',
            params={'phone': phone_number},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get('chat_id')
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to /api/telegram_user failed: {e}")
        return None

def get_order_summary(order):
    try:
        submitted_at = make_aware_if_naive(ensure_datetime(order.submitted_at))
        order_items_data = OrderItemSerializer(order.order_items.all(), many=True).data

        order_items_en, order_items_uk = [], []

        for item in order_items_data:
            common_data = {
                'size': item.get('size'),
                'quantity': item.get('quantity'),
                'price': item.get('price'),
                'color_value': item.get('color_value'),
            }

            # Determine the latest status and its timestamp
            latest_status_time, latest_status_key = None, None
            for status in STATUS_EMOJIS.keys():
                status_key = f"{status}_at"
                status_time = ensure_datetime(item.get(status_key))
                if status_time and (not latest_status_time or status_time > latest_status_time):
                    latest_status_time = status_time
                    latest_status_key = status_key

            order_items_en.append({
                **common_data,
                'name': item.get('name_en'),
                'color_name': item.get('color_name_en'),
                'collection_name': item.get('collection_name_en'),
            })
            order_items_uk.append({
                **common_data,
                'name': item.get('name_uk'),
                'color_name': item.get('color_name_uk'),
                'collection_name': item.get('collection_name_uk'),
            })

        return {
            'order_id': order.id,
            'order_items_en': order_items_en,
            'order_items_uk': order_items_uk,
            'submitted_at': datetime_to_str(submitted_at),
             latest_status_key: datetime_to_str(latest_status_time),
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
    phone_number = getattr(instance, 'phone', None)
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
                logger.info(f"Order ID {instance.id} removed from summary for chat ID {chat_id}")
            except OrderSummary.DoesNotExist:
                logger.warning(f"No summary found for chat ID {chat_id}")
