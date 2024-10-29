import requests
import logging
from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import is_aware, make_aware
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

def make_aware_if_naive(dt):
    """Converts a naive datetime to aware, using the current timezone."""
    if dt and not is_aware(dt):
        return make_aware(dt)  # Converts naive to aware
    return dt

def datetime_to_str(dt):
    """Converts a datetime object to string, ensuring it's aware."""
    dt = ensure_datetime(dt)
    if dt:
        dt = make_aware_if_naive(dt)  # Ensure it's aware before formatting
        return dt.strftime('%Y-%m-%d %H:%M')
    return None

def get_order_summary(order):
    """Generates a summary of an order."""
    submitted_at = ensure_datetime(order.submitted_at)
    created_at = ensure_datetime(order.created_at)
    processed_at = ensure_datetime(order.processed_at)
    complete_at = ensure_datetime(order.complete_at)
    canceled_at = ensure_datetime(order.canceled_at)
    status_fields = {
        'submitted_at': submitted_at,
        'created_at': created_at,
        'processed_at': processed_at,
        'complete_at': complete_at,
        'canceled_at': canceled_at,
    }
    latest_status_key = max(
        status_fields,
        key=lambda k: status_fields[k] or datetime.min
    )
    latest_status_time = status_fields[latest_status_key]

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
        latest_status_key: datetime_to_str(latest_status_time),  
        'submitted_at': datetime_to_str(submitted_at),
    }

    return summary

def update_order_summary(chat_id):
    """Updates the order summary for a specific chat_id."""
    try:
        orders = Order.objects.filter(telegram_user__chat_id=chat_id).prefetch_related('order_items__product')
        logger.info(f'Fetched {orders.count()} orders for chat ID: {chat_id}.')
        grouped_orders = []

        # Create summary for each order
        for order in orders:
            summary = get_order_summary(order)
            grouped_orders.append(summary)

        # Convert decimals if necessary
        converted_orders = [OrderSummary._convert_decimals(order) for order in grouped_orders]
        order_summary, created = OrderSummary.objects.update_or_create(
            chat_id=chat_id,
            defaults={'orders': converted_orders}
        )
        order_summary.orders = converted_orders  # Update orders field with converted values
        order_summary.save()

        logger.info("Order summary updated successfully for chat ID: {chat_id}.")

    except Exception as e:
        logger.error(f"Error updating order summary for chat ID {chat_id}: {str(e)}")

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
            update_order_summary(chat_id)
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
            update_order_summary(chat_id)
            logger.debug(f"OrderItem deleted for Order ID: {instance.order.id}, summary updated for chat ID: {chat_id}")

@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    """
    Signal that triggers after an Order instance is saved.
    Calls update_order_summary to update the OrderSummary records.
    """
    phone_number = instance.phone
    if phone_number:
        chat_id = get_chat_id_from_phone(phone_number)
        if chat_id:
            # Only call update_order_summary if the Order was created
            if created:
                update_order_summary(chat_id)
            logger.info(f"OrderSummary updated after Order (ID: {instance.id}) save.")
