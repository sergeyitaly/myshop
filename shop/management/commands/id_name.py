from django.core.management.base import BaseCommand
from shop.models import Product

class Command(BaseCommand):
    help = 'Regenerate ID names for all products'

    def handle(self, *args, **options):
        products = Product.objects.all()
        for product in products:
            if product.name and product.id:
                # Replace spaces with underscores in the name
                name_with_underscores = product.name.replace(' ', '_')
                product.id_name = f"{product.id}_{name_with_underscores}"
                try:
                    product.save(update_fields=['id_name'])
                    self.stdout.write(self.style.SUCCESS(f"Updated ID name for product {product.id}: {product.id_name}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error saving product {product.id}: {e}"))
            else:
                self.stdout.write(self.style.WARNING(f"Product {product.id} is missing a name or ID."))
        self.stdout.write(self.style.SUCCESS('Successfully updated ID names for all products.'))
