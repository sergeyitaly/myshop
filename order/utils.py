from django.utils import timezone
from order.models import Order
from .notifications import update_order_status_with_notification
from rest_framework.response import Response

def update_order_statuses():
    now = timezone.now()
    update_submitted_to_created(now)
    update_created_to_processed(now)
    update_processed_to_complete(now)

def update_submitted_to_created(now):
    orders = Order.objects.filter(status='submitted')
    for order in orders:
        submitted_at = order.submitted_at
        if submitted_at and (now - submitted_at).total_seconds() / 60 >= 1:
            chat_id = order.telegram_user.chat_id if order.telegram_user else None
            if chat_id:
                # Update order status to 'created'
                order.status = 'created'
                order.created_at = now  # Update created_at timestamp
                order.save()  # Save the order to the database

                # Prepare order items data
                order_items_data = [
                    {
                        "size": item.size,
                        "quantity": item.quantity,
                        "total_sum": item.total_sum,
                        "color_name": item.color_name,
                        "item_price": item.item_price,
                        "color_value": item.color_value,
                        "product_name": item.product_name,
                        "collection_name": item.collection_name,
                    }
                    for item in order.order_items.all()
                ]
                
                # Notify with the updated order status
                update_order_status_with_notification(
                    order.id,
                    order_items_data,
                    'created',
                    'created_at',
                    chat_id
                )

def update_created_to_processed(now):
    orders = Order.objects.filter(status='created')
    for order in orders:
        created_at = order.created_at
        if created_at and (now - created_at).total_seconds() / 60 >= 20:
            chat_id = order.telegram_user.chat_id if order.telegram_user else None
            if chat_id:
                # Update order status to 'processed'
                order.status = 'processed'
                order.processed_at = now  # Update processed_at timestamp
                order.save()  # Save the order to the database

                # Prepare order items data
                order_items_data = [
                    {
                        "size": item.size,
                        "quantity": item.quantity,
                        "total_sum": item.total_sum,
                        "color_name": item.color_name,
                        "item_price": item.item_price,
                        "color_value": item.color_value,
                        "product_name": item.product_name,
                        "collection_name": item.collection_name,
                    }
                    for item in order.order_items.all()
                ]
                
                # Notify with the updated order status
                update_order_status_with_notification(
                    order.id,
                    order_items_data,
                    'processed',
                    'processed_at',
                    chat_id
                )

def update_processed_to_complete(now):
    orders = Order.objects.filter(status='processed')
    for order in orders:
        processed_at = order.processed_at
        if processed_at and (now - processed_at).total_seconds() / 3600 >= 24:
            chat_id = order.telegram_user.chat_id if order.telegram_user else None
            if chat_id:
                # Update order status to 'complete'
                order.status = 'complete'
                order.complete_at = now  # Update complete_at timestamp
                order.save()  # Save the order to the database

                # Prepare order items data
                order_items_data = [
                    {
                        "size": item.size,
                        "quantity": item.quantity,
                        "total_sum": item.total_sum,
                        "color_name": item.color_name,
                        "item_price": item.item_price,
                        "color_value": item.color_value,
                        "product_name": item.product_name,
                        "collection_name": item.collection_name,
                    }
                    for item in order.order_items.all()
                ]
                
                # Notify with the updated order status
                update_order_status_with_notification(
                    order.id,
                    order_items_data,
                    'complete',
                    'complete_at',
                    chat_id
                )
