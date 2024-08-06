from django.core.management.base import BaseCommand
from order.utils import update_order_statuses

class Command(BaseCommand):
    help = 'Update order statuses'

    def handle(self, *args, **kwargs):
        update_order_statuses()
        self.stdout.write(self.style.SUCCESS('Successfully updated order statuses'))
