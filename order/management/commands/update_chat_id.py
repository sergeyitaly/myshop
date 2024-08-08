from django.core.management.base import BaseCommand
from order.models import Order, TelegramUser

class Command(BaseCommand):
    help = 'Updates chat_id for orders based on associated TelegramUser'

    def handle(self, *args, **kwargs):
        orders = Order.objects.filter(telegram_user__isnull=True)
        updated_count = 0

        for order in orders:
            try:
                telegram_user = TelegramUser.objects.get(phone=order.phone)
                order.telegram_user = telegram_user
                order.save(update_fields=['telegram_user'])
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f'Updated Order {order.id} with TelegramUser {telegram_user.id}'))
            except TelegramUser.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Order {order.id} does not have an associated TelegramUser'))

        self.stdout.write(self.style.SUCCESS(f'Finished updating chat_id for {updated_count} orders'))
