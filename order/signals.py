import requests
import logging
from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import is_aware, make_aware
from django.utils.dateparse import parse_datetime
from .models import Order, OrderSummary, OrderItem, TelegramUser
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

    # Create a summary that includes both the English and Ukrainian order items
    summary = {
        'order_id': order.id,
        'order_items_en': [
            {
                'size': item['size'] if item.get('size') else None,  # Handle optional size field
                'quantity': item['quantity'],
                'color_name': item['color_name'] if item.get('color_name') else None,
                'price': item['price'],
                'color_value': item['color_value'],
                'name': item['name'],
                'collection_name': item['collection_name'],
            } for item in order_items_data_en
        ],
        'order_items_uk': [
            {
                'size': item['size'] if item.get('size') else None,  # Handle optional size field
                'quantity': item['quantity'],
                'color_name': item['color_name'] if item.get('color_name') else None,
                'price': item['price'],
                'color_value': item['color_value'],
                'name': item['name'],
                'collection_name': item['collection_name'],
            } for item in order_items_data_uk
        ],
        latest_status_key: datetime_to_str(latest_status_time),  
        'submitted_at': datetime_to_str(submitted_at),
    }

    return summary



def update_order_summary(chat_id):
    """Updates the order summary for a specific chat_id."""
    try:
        # Fetch orders related to the provided chat_id and prefetch related order items and products
        orders = Order.objects.filter(telegram_user__chat_id=chat_id).prefetch_related('order_items__product')
        logger.info(f'Fetched {orders.count()} orders for chat ID: {chat_id}.')
        
        # Grouping the order summaries
        grouped_orders = []
        for order in orders:
            summary = get_order_summary(order)
            grouped_orders.append(summary)

        # Convert orders to the appropriate format for storage
        order_summary_instance = OrderSummary()
        converted_orders = order_summary_instance._convert_decimals(data=grouped_orders)

        # Update or create the OrderSummary object for the provided chat_id
        # The 'orders' field will be updated with the converted orders data
        order_summary, created = OrderSummary.objects.update_or_create(
            chat_id=chat_id,
            defaults={'orders': converted_orders}
        )

        # Clear any cached order summary for the chat_id to ensure freshness
        cache.delete(f'order_summary_{chat_id}')
        logger.info(f"Order summary updated successfully for chat ID: {chat_id}.")

    except Exception as e:
        # Log any error that occurs during the update process
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


def has_order_summary_changed(order_summary, order):
    """
    Determines if the order summary has changed and needs updating.
    This is a basic implementation. You can refine it to check specific fields that would indicate a change.
    """
    # For example, check if the order status or items have changed
    if order_summary.orders != get_order_summary(order):
        return True
    return False


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    if created or instance.status in ['processed', 'complete', 'canceled']:
        # Ensure the order is associated with a TelegramUser and chat_id is correctly populated
        if not instance.telegram_user:
            try:
                telegram_user = TelegramUser.objects.get(phone=instance.phone)
                instance.telegram_user = telegram_user
                instance.save()
                logger.info(f'Order {instance.id} linked to TelegramUser {telegram_user.id}.')
            except TelegramUser.DoesNotExist:
                logger.warning(f'TelegramUser not found for phone {instance.phone}.')
        
        # Update order summary if the TelegramUser is set and the chat_id is valid
        if instance.telegram_user and instance.telegram_user.chat_id:
            # Prevent unnecessary updates by checking if the order summary needs updating
            try:
                order_summary = OrderSummary.objects.get(chat_id=instance.telegram_user.chat_id)
                # Check if the orders have changed since the last update (you can modify this logic if needed)
                if has_order_summary_changed(order_summary, instance):
                    update_order_summary(instance.telegram_user.chat_id)
                    logger.info(f"Order summary updated for chat_id {instance.telegram_user.chat_id}.")
                else:
                    logger.info(f"Order summary not updated for chat_id {instance.telegram_user.chat_id} (no changes).")
            except OrderSummary.DoesNotExist:
                update_order_summary(instance.telegram_user.chat_id)
                logger.info(f"Order summary created for chat_id {instance.telegram_user.chat_id}.")



