from django.core.management.base import BaseCommand
from shop.tasks import increase_stock_for_unavailable_products  # Import the Celery task

class Command(BaseCommand):
    help = "Trigger stock update for all unavailable products"

    def handle(self, *args, **kwargs):
        increase_stock_for_unavailable_products.apply_async()
        self.stdout.write(self.style.SUCCESS("Triggered stock update for unavailable products via Celery task"))
