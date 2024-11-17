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
    """Ensure the value is a datetime object."""
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    raise ValueError("Invalid datetime value")

def make_aware_if_naive(dt):
    """Converts a naive datetime to aware, using the current timezone."""
    if dt and not is_aware(dt):
        return make_aware(dt)
    return dt

def datetime_to_str(dt):
    """Converts a datetime object to string, ensuring it's aware."""
    dt = ensure_datetime(dt)
    if dt:
        dt = make_aware_if_naive(dt)
        return dt.strftime('%Y-%m-%d %H:%M')
    return None

def get_order_summary(order):
    """Generates a summary of an order, including details in both English and Ukrainian."""
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

def update_order_summary():
    """Updates the summary of orders grouped by Telegram chat ID."""
    try:
        # Prefetch related data to optimize database queries
        orders = Order.objects.prefetch_related('order_items__product', 'telegram_user').all()
        logger.info(f'Fetched {orders.count()} orders.')
        grouped_orders = {}

        # Group orders by chat_id to minimize updates
        for order in orders:
            order_chat_id = order.telegram_user.chat_id if order.telegram_user else None
            if not order_chat_id:
                continue

            if order_chat_id not in grouped_orders:
                grouped_orders[order_chat_id] = []

            summary = get_order_summary(order)
            existing_summary = next((o for o in grouped_orders[order_chat_id] if o['order_id'] == order.id), None)

            if existing_summary:
                # Update the existing summary with new order details
                existing_summary.update(summary)
            else:
                # Append the new summary if it doesn't exist
                grouped_orders[order_chat_id].append(summary)

        # Bulk update or create order summaries
        order_summary_objects = []
        for chat_id, orders_summary in grouped_orders.items():
            order_summary_objects.append(OrderSummary(chat_id=chat_id, orders=orders_summary))

        # Use bulk_create for creating or updating the OrderSummary
        OrderSummary.objects.bulk_create(order_summary_objects, ignore_conflicts=True)
        logger.info(f'Order summaries created/updated for chat IDs: {", ".join(grouped_orders.keys())}')

        # Clear the cache for each updated order summary
        for chat_id in grouped_orders:
            cache.delete(f'order_summary_{chat_id}')

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

@receiver(post_save, sender=Order)
def update_order_summary_on_order_status_change(sender, instance, **kwargs):
    """Updates the order summary when the order is saved or its status changes."""
    chat_id = instance.telegram_user.chat_id if instance.telegram_user else None
    if chat_id:
        update_order_summary()  # Optimized version will be called here
        logger.debug(f"Order status or details updated for Order ID: {instance.id}, summary updated for chat ID: {chat_id}")
        
@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_summary_on_order_item_change(sender, instance, **kwargs):
    """Updates the order summary when an OrderItem is added, updated, or deleted."""
    chat_id = instance.order.telegram_user.chat_id if instance.order.telegram_user else None
    if chat_id:
        update_order_summary()  # Optimized version will be called here
        logger.debug(f"OrderItem change detected for Order ID: {instance.order.id}, summary updated for chat ID: {chat_id}")

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
            update_order_summary()  # Optimized version will be called here
            logger.debug(f"OrderItem deleted for Order ID: {instance.order.id}, summary updated for chat ID: {chat_id}")
