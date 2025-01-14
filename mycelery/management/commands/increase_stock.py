from django.core.management.base import BaseCommand
from shop.models import Product

class Command(BaseCommand):
    help = "Increase stock for all unavailable products"

    def handle(self, *args, **kwargs):
        # Perform a bulk update for all unavailable products
        updated_count = Product.objects.filter(available=False).update(stock=10, available=True)
        
        # Log the result
        if updated_count > 0:
            self.stdout.write(self.style.SUCCESS(f"Updated stock for {updated_count} unavailable products."))
        else:
            self.stdout.write(self.style.WARNING("No unavailable products found to update."))
