from django.core.management.base import BaseCommand
from order.tasks import update_order_statuses  # Import the Celery task

class Command(BaseCommand):
    help = "Trigger update of order statuses based on time periods and send notifications"
    def handle(self, *args, **kwargs):
        update_order_statuses.apply_async()
        self.stdout.write(self.style.SUCCESS("Triggered the update of order statuses via Celery task"))
