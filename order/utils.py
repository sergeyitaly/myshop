from django.utils import timezone
from order.models import Order, OrderSummary
from .notifications import update_order_status_with_notification
from django.utils.dateformat import format as date_format
from django.db import transaction
from django.utils.translation import gettext as _  # Import gettext for translation
import requests
from django.conf import settings
from .models import *

def update_order_statuses():
    now = timezone.now()
    update_orders('submitted', 'created', 1, 'submitted_at', now)
    update_orders('created', 'processed', 20, 'created_at', now)
    update_orders('processed', 'complete', 24 * 60, 'processed_at', now)

def update_orders(current_status, new_status, threshold_minutes, timestamp_field, now):
    orders = Order.objects.filter(status=current_status)
    for order in orders:
        order_timestamp = getattr(order, timestamp_field)
        if order_timestamp and (now - order_timestamp).total_seconds() / 60 >= threshold_minutes:
            chat_id = order.telegram_user.chat_id if order.telegram_user else None
            if chat_id:
                # Update the order status and corresponding timestamp
                language = order.language   
                update_order_status(order, new_status, now, timestamp_field)
                order_summary = prepare_order_summary(order)
                with transaction.atomic():
                    order_summary_instance, created = OrderSummary.objects.update_or_create(
                        chat_id=chat_id,
                        defaults={
                            'orders': order_summary["order_items"],  # Ensure this matches your OrderSummary model
                            'latest_status': order_summary["latest_status"],  # Optionally store latest status
                            'latest_status_time': order_summary["latest_status_time"],  # Include latest status timestamp
                        }
                    )
                    update_order_status_with_notification(
                        order.id,
                        order_summary["order_items"],
                        new_status,
                        f'{new_status}_at',
                        chat_id,
                        language
                    )

def update_order_status(order, new_status, now, timestamp_field):
    order.status = new_status
    setattr(order, f'{new_status}_at', now)  # Dynamically set the timestamp for the new status
    order.save()

def prepare_order_summary(order):
    order_items_data_en = []
    order_items_data_uk = []

    for item in order.order_items.all():
        order_items_data_en.append({
            "size": item.size,
            "quantity": item.quantity,
            "color_name": item.color_name_en if item.color_name_en else _("No Color"),
            "currency" : item.currency,
            "item_price": float(item.item_price),
            "color_value": item.color_value,
            "product_name": item.product_name_en if item.product_name_en else _("No Name"),
            "collection_name": item.collection_name_en if item.collection_name_en else _("No Collection"),
        })

        order_items_data_uk.append({
            "size": item.size,
            "quantity": item.quantity,
            "color_name": item.color_name_uk if item.color_name_uk else _("No Color"),
            "item_price": float(item.item_price),
            "currency" : item.currency,
            "color_value": item.color_value,
            "product_name": item.product_name_uk if item.product_name_uk else _("No Name"),
            "collection_name": item.collection_name_uk if item.collection_name_uk else _("No Collection"),
        })

    status_mapping = {
        'created': (order.created_at, _('Created')),
        'processed': (order.processed_at, _('Processed')),
        'completed': (order.complete_at, _('Completed')),
        'canceled': (order.canceled_at, _('Canceled')),
    }

    latest_status = None
    latest_status_time = None

    for status, (timestamp, status_name) in status_mapping.items():
        if timestamp:
            if latest_status_time is None or timestamp > latest_status_time:
                latest_status_time = timestamp
                latest_status = status_name

    # Prepare the order summary
    summary = {
        'order_id': order.id,
        'order_items_en': order_items_data_en,
        'order_items_uk': order_items_data_uk,
        latest_status : datetime_to_str(latest_status_time),
        'submitted_at': datetime_to_str(order.submitted_at),
    }

    return summary

def datetime_to_str(dt):
    """Convert a datetime object to a formatted string."""
    return date_format(dt, 'Y-m-d H:i') if dt else None

def send_mass_message_with_logging(telegram_message):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    base_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    website_url = settings.VERCEL_DOMAIN

    users = TelegramUser.objects.all()
    sent_users = []

    for user in users:
        message_with_link = (
            f"{telegram_message.content}\n\n"
            f"<a href='{website_url}'>Visit our website</a>"
        )

        payload = {
            'chat_id': user.chat_id,
            'text': message_with_link,
            'parse_mode': 'HTML',  # Enable HTML to render the link
        }

        try:
            response = requests.post(base_url, json=payload)
            response.raise_for_status()  # Raise an error for failed requests
            sent_users.append(user)
        except requests.exceptions.RequestException as e:
            print(f"Failed to send message to {user.chat_id}: {e}")

    telegram_message.sent_to.add(*sent_users)  # Log the sent users
