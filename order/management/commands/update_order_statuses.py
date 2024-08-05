from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from order.models import Order
from order.signals import update_order_status_with_notification

class Command(BaseCommand):
    help = 'Update order statuses based on time intervals'

    def handle(self, *args, **kwargs):
        self.update_submitted_to_created()
        self.update_created_to_processed()
        self.update_processed_to_complete()

    def update_submitted_to_created(self):
        orders = Order.objects.filter(status='submitted')
        now = timezone.now()
        for order in orders:
            submitted_at = order.submitted_at
            if submitted_at and (now - submitted_at).total_seconds() / 60 >= 10:
                self.stdout.write(f"Updating Order ID {order.id} from 'submitted' to 'created'.")
                update_order_status_with_notification(order, 'created', 'created_at')

    def update_created_to_processed(self):
        orders = Order.objects.filter(status='created')
        now = timezone.now()
        for order in orders:
            created_at = order.created_at
            if created_at and (now - created_at).total_seconds() / 60 >= 20:
                self.stdout.write(f"Updating Order ID {order.id} from 'created' to 'processed'.")
                update_order_status_with_notification(order, 'processed', 'processed_at')

    def update_processed_to_complete(self):
        orders = Order.objects.filter(status='processed')
        now = timezone.now()
        for order in orders:
            processed_at = order.processed_at
            if processed_at and (now - processed_at).total_seconds() / 3600 >= 24:
                self.stdout.write(f"Updating Order ID {order.id} from 'processed' to 'complete'.")
                update_order_status_with_notification(order, 'complete', 'complete_at')
