# your_app/management/commands/set_webhook.py

from django.core.management.base import BaseCommand
from order.views import set_telegram_webhook

class Command(BaseCommand):
    help = 'Sets the Telegram webhook'

    def handle(self, *args, **options):
        try:
            set_telegram_webhook()
            self.stdout.write(self.style.SUCCESS('Webhook successfully set.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error setting webhook: {e}'))
