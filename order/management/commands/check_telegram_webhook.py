# order/management/commands/check_telegram_webhook.py

from django.core.management.base import BaseCommand
from django.conf import settings
import requests

class Command(BaseCommand):
    help = 'Check the status of the Telegram webhook'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Checking Telegram webhook status...'))
        self.get_telegram_webhook_info()

    def get_telegram_webhook_info(self):
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getWebhookInfo"
        try:
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
            self.stdout.write(self.style.SUCCESS(f'Webhook info: {result}'))
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Failed to get webhook info: {e}"))
