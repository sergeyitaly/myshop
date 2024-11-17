import requests
import logging
from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import is_aware, make_aware
from order.models import Order, OrderSummary, OrderItem, TelegramUser
from order.serializers import OrderItemSerializer
from django.core.cache import cache

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
        return datetime.fromisoformat(value)
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

def get_order_summary(order):
    submitted_at = make_aware_if_naive(ensure_datetime(order.submitted_at))
    created_at = make_aware_if_naive(ensure_datetime(order.created_at))
    processed_at = make_aware_if_naive(ensure_datetime(order.processed_at))
    complete_at = make_aware_if_naive(ensure_datetime(order.complete_at))
    canceled_at = make_aware_if_naive(ensure_datetime(order.canceled_at))

    status_fields = {
        'submitted_at': submitted_at,
        'created_at': created_at,
        'processed_at': processed_at,
        'complete_at': complete_at,
        'canceled_at': canceled_at,
    }
    latest_status_key = max(
        status_fields,
        key=lambda k: status_fields[k] or make_aware_if_naive(datetime.min)
    )
    latest_status_time = status_fields[latest_status_key]
    order_items_data_en = OrderItemSerializer(order.order_items.filter(language='en'), many=True).data
    order_items_data_uk = OrderItemSerializer(order.order_items.filter(language='uk'), many=True).data
    summary = {
        'order_id': order.id,
        'order_items_en': [
            {
                'size': item.get('size'),
                'quantity': item.get('quantity'),
                'color_name': item.get('color_name'),
                'price': item.get('price'),
                'color_value': item.get('color_value'),
                'name': item.get('name'),
                'collection_name': item.get('collection_name'),
            } for item in order_items_data_en
        ],
        'order_items_uk': [
            {
                'size': item.get('size'),
                'quantity': item.get('quantity'),
                'color_name': item.get('color_name'),
                'price': item.get('price'),
                'color_value': item.get('color_value'),
                'name': item.get('name'),
                'collection_name': item.get('collection_name'),
            } for item in order_items_data_uk
        ],
        latest_status_key: datetime_to_str(latest_status_time),
        'submitted_at': datetime_to_str(submitted_at),
    }
    return summary

def validate_telegram_user(telegram_user):
    if not telegram_user or not telegram_user.chat_id:
        logger.warning("Invalid Telegram user or missing chat_id.")
        return False
    return True


def update_order_summary():
    try:
        orders = Order.objects.prefetch_related('order_items__product').all()
        grouped_orders = {}

        for order in orders:
            telegram_user = order.telegram_user
            if not validate_telegram_user(telegram_user):
                logger.warning(f"Skipping order {order.id}: Invalid Telegram user or missing chat_id.")
                continue

            chat_id = telegram_user.chat_id
            if chat_id not in grouped_orders:
                grouped_orders[chat_id] = []

            summary = get_order_summary(order)
            grouped_orders[chat_id].append(summary)

        for chat_id, orders_summary in grouped_orders.items():
            OrderSummary.objects.update_or_create(
                chat_id=chat_id,
                defaults={'orders': orders_summary}
            )
            logger.info(f"Order summaries created/updated for chat ID {chat_id}")

    except Exception as e:
        logger.error(f"Error while generating order summaries: {e}")


def get_chat_id_from_phone(phone_number):
    try:
        response = requests.get(f'{settings.VERCEL_DOMAIN}/api/telegram_users', params={'phone': phone_number})
        response.raise_for_status()
        response_json = response.json()
        if not isinstance(response_json, dict):
            logger.error(f"Unexpected response format: {response.text}")
            return None
        return response_json.get('chat_id')
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to /api/telegram_users failed: {e}")
        return None
    except ValueError as e:
        logger.error(f"Invalid JSON response: {e}")
        return None



@receiver(post_save, sender=OrderItem)
def update_order_summary_on_order_item_change(sender, instance, **kwargs):
    phone_number = instance.order.phone
    if phone_number:
        chat_id = get_chat_id_from_phone(phone_number)
        if chat_id:
            order = instance.order
            previous_status = instance.__class__.objects.get(id=instance.id).status if instance.pk else None
            status_changed = instance.order.status != previous_status
            if status_changed or has_meaningful_item_changes(instance, order):
                update_order_summary()  # Trigger the summary update
                logger.debug(f"OrderItem updated for Order ID: {instance.order.id}, summary updated for chat ID: {chat_id}")
            else:
                logger.debug(f"No significant changes in OrderItem for Order ID: {instance.order.id}. Skipping summary update.")


@receiver(post_save, sender=Order)
def update_order_summary_on_order_status_change(sender, instance, **kwargs):
    phone_number = instance.phone
    if phone_number:
        chat_id = get_chat_id_from_phone(phone_number)
        if chat_id:
            # If the order status has changed, trigger summary update
            update_order_summary()
            logger.debug(f"Order status updated for Order ID: {instance.id}, summary updated for chat ID: {chat_id}")


def has_meaningful_item_changes(instance, order):
    original_item = OrderItem.objects.get(id=instance.id) if instance.pk else None
    if original_item:
        return (
            original_item.quantity != instance.quantity or
            original_item.price != instance.price or
            original_item.size != instance.size or
            original_item.color_name != instance.color_name
        )
    return False

@receiver(post_delete, sender=Order)
def remove_order_from_summary(sender, instance, **kwargs):
    phone_number = instance.phone
    if phone_number:
        chat_id = get_chat_id_from_phone(phone_number)
        if chat_id:
            try:
                order_summary = OrderSummary.objects.get(chat_id=chat_id)
                updated_orders = [o for o in order_summary.orders if o['order_id'] != instance.id]
                if len(updated_orders) != len(order_summary.orders):
                    order_summary.orders = updated_orders
                    order_summary.save()
                    logger.debug(f"Removed order ID {instance.id} from summary for chat ID {chat_id}")
                else:
                    logger.debug(f"No change in order summary for chat ID {chat_id} (order ID {instance.id} already removed)")
                cache_key = f'order_summary_{chat_id}'
                if cache.get(cache_key):
                    cache.delete(cache_key)
                    logger.debug(f"Cache for order summary {cache_key} deleted")
                else:
                    logger.warning(f"Cache for order summary {cache_key} not found (not deleted)")

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
