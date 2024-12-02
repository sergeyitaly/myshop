# management/commands/link_telegram_users.py
from django.core.management.base import BaseCommand
from order.models import Order, TelegramUser

class Command(BaseCommand):
    help = "Link Telegram users to existing orders based on phone number"

    def handle(self, *args, **kwargs):
        orders = Order.objects.filter(telegram_user__isnull=True, phone__isnull=False)
        updated_count = 0

        for order in orders:
            try:
                telegram_user = TelegramUser.objects.get(phone=order.phone)
                order.telegram_user = telegram_user
                order.save()
                updated_count += 1
            except TelegramUser.DoesNotExist:
                self.stdout.write(f"No Telegram user found for phone: {order.phone}")

        self.stdout.write(f"Updated {updated_count} orders with Telegram users.")
