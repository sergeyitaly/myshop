from django.core.management.base import BaseCommand
from order.models import Order, TelegramUser
from django.db import IntegrityError, transaction

class Command(BaseCommand):
    help = 'Associates TelegramUsers to Orders based on phone number.'

    def handle(self, *args, **kwargs):
        orders_without_telegram = Order.objects.filter(telegram_user__isnull=True)  # Orders without a TelegramUser
        total_orders = orders_without_telegram.count()

        if total_orders == 0:
            self.stdout.write(self.style.SUCCESS('No orders without TelegramUser association.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Total orders to process: {total_orders}'))

        # Iterate through orders that don't have an associated TelegramUser
        for order in orders_without_telegram:
            phone = order.phone  # Assuming 'phone' exists on the Order model
            if not phone:
                self.stdout.write(self.style.WARNING(f'Order {order.id} does not have a phone number, skipping.'))
                continue

            try:
                # Try to get the TelegramUser based on the phone number
                telegram_user = TelegramUser.objects.get(phone=phone)

                # Log the found telegram_user
                self.stdout.write(self.style.SUCCESS(f'Found TelegramUser: {telegram_user.id}'))

                # Associate the TelegramUser with the order
                order.telegram_user = telegram_user
                order.save()

                self.stdout.write(self.style.SUCCESS(f'Successfully associated TelegramUser {telegram_user.id} with order {order.id}'))

            except TelegramUser.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'No TelegramUser found for phone {phone}, skipping order {order.id}.'))

            except IntegrityError:
                # Handle any integrity errors (e.g., unique constraints, etc.)
                self.stdout.write(self.style.ERROR(f'Error associating TelegramUser with order {order.id}.'))
