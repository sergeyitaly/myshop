from django.core.management.base import BaseCommand
from order.models import Order, TelegramUser
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Link orders to Telegram users based on phone numbers'

    def handle(self, *args, **kwargs):
        orders = Order.objects.filter(telegram_user__isnull=True)
        if not orders.exists():
            self.stdout.write("No unlinked orders found.")
            return

        self.stdout.write(f"Found {orders.count()} orders without TelegramUser.")
        for order in orders:
            try:
                telegram_user = TelegramUser.objects.get(phone=order.phone)
                order.telegram_user = telegram_user
                order.save(update_fields=['telegram_user'])
                message = f"Linked Order ID {order.id} to TelegramUser ID {telegram_user.id} (Phone: {telegram_user.phone})"
                self.stdout.write(message)
                logger.info(message)
            except TelegramUser.DoesNotExist:
                message = f"No TelegramUser found for Order ID {order.id} (Phone: {order.phone})"
                self.stdout.write(message)
                logger.warning(message)
