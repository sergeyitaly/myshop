from django.core.management.base import BaseCommand
from django.db import transaction
from shop.models import Product  # Adjust this import if necessary

class Command(BaseCommand):
    help = 'Fix duplicate slugs in the Product model'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        products = Product.objects.all().order_by('slug')
        prev_slug = None
        for product in products:
            if product.slug == prev_slug:
                product.slug += f'-{product.pk}'  # Append product ID to make slug unique
                product.save()
            prev_slug = product.slug
        self.stdout.write(self.style.SUCCESS('Successfully fixed duplicate slugs'))
