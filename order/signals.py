import requests
import logging
from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import is_aware, make_aware
from order.models import Order, OrderSummary, OrderItem, TelegramUser
from order.serializers import OrderItemSerializer

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

def update_order_summary(chat_id):
    """Ensure the order summary for a specific chat ID is updated correctly."""
    try:
        # Fetch the orders for the given chat ID, prefetch related order items and products
        orders = Order.objects.filter(telegram_user__chat_id=chat_id).prefetch_related('order_items__product')

        # Fetch or create the order summary for the given chat ID
        order_summary_instance, created = OrderSummary.objects.get_or_create(chat_id=chat_id)

        # Group orders by their relevant details using a helper function
        grouped_orders = [get_order_summary(order) for order in orders]

        # If it's a new OrderSummary, directly set and save the grouped orders
        if created:
            order_summary_instance.orders = grouped_orders
            order_summary_instance.save()
            logger.debug(f"Order summary created for chat ID {chat_id}")
        else:
            # For existing OrderSummary, merge the orders list without losing the existing ones
            existing_order_ids = {order['order_id'] for order in order_summary_instance.orders}

            # Filter out new orders that are not present in the existing summary
            updated_orders = [
                order for order in grouped_orders
                if order['order_id'] not in existing_order_ids
            ]
            
            # Merge the updated orders with existing ones (if applicable)
            order_summary_instance.orders.extend(updated_orders)
            order_summary_instance.save()
            logger.debug(f"Order summary updated for chat ID {chat_id}")

        # Clear cache for this chat_id to ensure up-to-date information is fetched
        cache.delete(f'order_summary_{chat_id}')
        
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
    """Update order summary when an order item is updated."""
    try:
        # Get the chat_id from the phone number
        phone_number = instance.order.phone
        chat_id = get_chat_id_from_phone(phone_number)
        
        if chat_id:
            update_order_summary(chat_id)
            logger.debug(f"OrderItem updated for Order ID: {instance.order.id}, summary updated for chat ID: {chat_id}")
    except Exception as e:
        logger.error(f"Error updating order summary on order item change: {e}")

@receiver(post_delete, sender=OrderItem)
def update_order_summary_on_order_item_delete(sender, instance, **kwargs):
    """Update order summary when an order item is deleted."""
    try:
        # Get the chat_id from the phone number
        phone_number = instance.order.phone
        chat_id = get_chat_id_from_phone(phone_number)
        
        if chat_id:
            update_order_summary(chat_id)
            logger.debug(f"OrderItem deleted for Order ID: {instance.order.id}, summary updated for chat ID: {chat_id}")
    except Exception as e:
        logger.error(f"Error updating order summary on order item delete: {e}")

@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    """Handle the post-save for the Order model."""
    try:
        if created or instance.status in ['processed', 'complete', 'canceled']:
            # Link to TelegramUser if not already done
            if not instance.telegram_user:
                try:
                    telegram_user = TelegramUser.objects.get(phone=instance.phone)
                    instance.telegram_user = telegram_user
                    instance.save()
                    logger.info(f'Order {instance.id} linked to TelegramUser {telegram_user.id}.')
                except TelegramUser.DoesNotExist:
                    logger.warning(f'TelegramUser not found for phone {instance.phone}.')

            if instance.telegram_user and instance.telegram_user.chat_id:
                # Update the order summary for the related Telegram user's chat ID
                update_order_summary(instance.telegram_user.chat_id)
                logger.info(f'Order {instance.id} saved, order summary updated for chat ID {instance.telegram_user.chat_id}')
    except Exception as e:
        logger.error(f"Error saving order and updating summary: {e}")


@receiver(post_delete, sender=Order)
def remove_order_from_summary(sender, instance, **kwargs):
    """Remove an order from the summary when it is deleted."""
    try:
        phone_number = instance.phone
        chat_id = get_chat_id_from_phone(phone_number)
        if chat_id:
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

