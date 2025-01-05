from django.utils import timezone
from order.models import Order, OrderSummary
from .notifications import update_order_status_with_notification
from django.utils.dateformat import format as date_format
from django.db import transaction
from django.utils.translation import gettext as _  # Import gettext for translation
import requests
from django.conf import settings
from .models import *
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from order.models import Order

@shared_task
def update_order_statuses():
    now = timezone.now()

    def update_orders(current_status, new_status, minutes, status_field):
        threshold_time = now - timedelta(minutes=minutes)
        orders_to_update = Order.objects.filter(
            status=current_status,
            **{f"{status_field}__lte": threshold_time}
        )
        updated_count = orders_to_update.update(
            status=new_status,
            **{f"{new_status}_at": now}
        )
        return updated_count

    submitted_to_created = update_orders(
        current_status='submitted',
        new_status='created',
        minutes=1,
        status_field='submitted_at'
    )
    created_to_processed = update_orders(
        current_status='created',
        new_status='processed',
        minutes=20,
        status_field='created_at'
    )
    processed_to_complete = update_orders(
        current_status='processed',
        new_status='complete',
        minutes=24 * 60,  
        status_field='processed_at'
    )

    return {
        'submitted_to_created': submitted_to_created,
        'created_to_processed': created_to_processed,
        'processed_to_complete': processed_to_complete,
    }


def datetime_to_str(dt):
    return date_format(dt, 'Y-m-d H:i') if dt else None

def send_mass_message_with_logging(telegram_message):
    bot_token = settings.NOTIFICATIONS_API
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
            'parse_mode': 'HTML',
        }

        try:
            response = requests.post(base_url, json=payload)
            response.raise_for_status()
            sent_users.append(user)
        except requests.exceptions.RequestException as e:
            print(f"Failed to send message to {user.chat_id}: {e}")

    telegram_message.sent_to.add(*sent_users) 
