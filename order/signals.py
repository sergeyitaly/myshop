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
    # Convert the necessary datetime fields to naive datetimes
    submitted_at = safe_make_naive(order.submitted_at)
    last_status_time = safe_make_naive(
        order.canceled_at or order.complete_at or order.processed_at or order.created_at or order.submitted_at
    )

    # Serialize the order items
    order_items_data = OrderItemSerializer(order.order_items.all(), many=True).data

    # Format the summary dictionary to match the required JSON structure
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
        'last_status': order.status,
        'last_status_time': datetime_to_str(last_status_time),
        'submitted_at': datetime_to_str(submitted_at)
    }

    return summary


def update_order_summary_for_chat_id():
    try:
        # Fetch all orders with related order items and products
        orders = Order.objects.prefetch_related('order_items__product').all()
        logger.info(f'Fetched {orders.count()} orders.')

        # Group orders by chat_id
        grouped_orders = {}
        for order in orders:
            chat_id = order.telegram_user.chat_id if order.telegram_user else None
            if chat_id not in grouped_orders:
                grouped_orders[chat_id] = []

            # Extract and format datetime fields
            submitted_at = safe_make_naive(order.submitted_at)
            created_at = safe_make_naive(order.created_at)
            processed_at = safe_make_naive(order.processed_at)
            complete_at = safe_make_naive(order.complete_at)
            canceled_at = safe_make_naive(order.canceled_at)

            # Determine the latest timestamp directly using datetime
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

            # Convert datetime to string for summary
            def datetime_to_str(dt):
                if dt:
                    return dt.strftime('%Y-%m-%d %H:%M')
                return None

            # Serialize the order
            serializer = OrderSerializer(order)
            order_data = serializer.data

            # Create the summary for the order
            summary = {
                'order_id': order.id,
                'order_items': order_data['order_items'],
                'submitted_at': datetime_to_str(submitted_at),
                latest_status_field: datetime_to_str(latest_status_timestamp)
            }
            # Check if this order already exists in the summary for the chat_id
            existing_summary = next((o for o in grouped_orders[chat_id] if o['order_id'] == order.id), None)
            if existing_summary:
                # If the order already exists, update the existing summary
                grouped_orders[chat_id].remove(existing_summary)
            
            # Append the updated summary to the grouped orders
            grouped_orders[chat_id].append(summary)

        # Log grouped orders for debugging
        logger.info(f'Grouped Orders: {grouped_orders}')

        # Update OrderSummary
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

#def update_order_summary_for_phone(phone_number):
#    chat_id = get_chat_id_from_phone(phone_number)
#    if chat_id:
#        update_order_summary_for_chat_id(chat_id)
#    else:
#        logger.error(f"Failed to update order summary for phone number: {phone_number}")


#def get_random_saying(file_path):
#    if not os.path.exists(file_path):
#        logger.error(f"Failed to read sayings file: [Errno 2] No such file or directory: '{file_path}'")
#        return "No sayings available."
#    
#    try:
#        with open(file_path, 'r', encoding='utf-8') as file:
#            sayings = [line.strip() for line in file if line.strip()]
#        
#        if not sayings:
#            logger.error("Sayings file is empty.")
#            return "No sayings available."
#        
#        return random.choice(sayings)
#    except Exception as e:
#        logger.error(f"Error reading sayings file: {e}")
#        return "No sayings available."

@receiver(post_save, sender=Order)
def update_order_summary(sender, instance, **kwargs):
    # Only update the summary if the order is created or updated
    if kwargs.get('created', False) or kwargs.get('update_fields'):
        phone_number = instance.phone
        if phone_number:
            chat_id = get_chat_id_from_phone(phone_number)
            if chat_id:
                update_order_summary_for_chat_id()
            else:
                # Handle case where chat_id is not found for the phone number
                logger.error(f"No chat_id found for phone number: {phone_number}")
        else:
            # Handle orders with no phone number
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

                # Retrieve the OrderSummary instance
                order_summary = OrderSummary.objects.get(chat_id=chat_id)
                
                # Update the orders list to exclude the deleted order
                updated_orders = [order for order in order_summary.orders if order['order_id'] != instance.id]
                
                # Update the OrderSummary instance with the new orders list
                order_summary.orders = updated_orders
                
                # Save the updated OrderSummary instance
                order_summary.save()
                
                # Invalidate the cache
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

#def update_order_summary_for_chat_id(chat_id):
#    try:
#        orders = Order.objects.filter(telegram_user__chat_id=chat_id)
#        summary = []
#        for order in orders:
#            serializer = OrderSerializer(order)
#            order_data = serializer.data
#            summary.append({
#                'order_id': order.id,
#                'order_items': order_data['order_items'],
#                'submitted_at': order.submitted_at.strftime('%Y-%m-%d %H:%M') if order.submitted_at else None,
#                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M') if order.created_at else None,
#                'processed_at': order.processed_at.strftime('%Y-%m-%d %H:%M') if order.processed_at else None,
#                'complete_at': order.complete_at.strftime('%Y-%m-%d %H:%M') if order.complete_at else None,
#                'canceled_at': order.canceled_at.strftime('%Y-%m-%d %H:%M') if order.canceled_at else None,
#            })
#
#        OrderSummary.objects.update_or_create(
#            chat_id=chat_id,
#            defaults={'orders': summary}
#        )
#        logger.info(f'Order summary updated for chat ID {chat_id}')
#    
#    except Exception as e:
#        logger.error(f'Error updating order summary for chat ID {chat_id}: {e}')
