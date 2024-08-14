import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from shop.models import Category, Collection, Product, AdditionalField  # Adjust import to your models

class Command(BaseCommand):
    help = 'Import data from CSV files and update related fields in the database'

    def handle(self, *args, **options):
        self.import_categories()
        self.import_collections()
        self.import_products()
        self.import_additional_fields()

    def import_categories(self):
        with open('categories.csv', 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            with transaction.atomic():
                for row in reader:
                    category_id = row['id']
                    name = row['name']
                    Category.objects.update_or_create(
                        id=category_id,
                        defaults={'name_uk': name}
                    )
        self.stdout.write(self.style.SUCCESS('Successfully imported categories from categories.csv'))

    def import_collections(self):
        with open('collections.csv', 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            with transaction.atomic():
                for row in reader:
                    collection_id = row['id']
                    name = row['name']
                    Collection.objects.update_or_create(
                        id=collection_id,
                        defaults={'name_uk': name}
                    )
        self.stdout.write(self.style.SUCCESS('Successfully imported collections from collections.csv'))

    def import_products(self):
        with open('products.csv', 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            with transaction.atomic():
                for row in reader:
                    product_id = row['id']
                    name = row['name']
                    description = row['description']
                    color_name = row['color_name']
                    
                    # Ensure the collection and category IDs exist
                    collection_id = row.get('collection_id')
                    if collection_id:
                        collection_id = int(collection_id)
                    
                    Product.objects.update_or_create(
                        id=product_id,
                        defaults={
                            'name_uk': name,
                            'description_uk': description,
                            'color_name_uk': color_name,
                            'collection_id': collection_id
                        }
                    )
        self.stdout.write(self.style.SUCCESS('Successfully imported products from products.csv'))

    def import_additional_fields(self):
        with open('additional_fields.csv', 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            with transaction.atomic():
                for row in reader:
                    additional_field_id = row['id']
                    name = row['name']
                    value = row['value']
                    product_id = row['product_id']
                    
                    # Ensure the product exists
                    if Product.objects.filter(id=product_id).exists():
                        AdditionalField.objects.update_or_create(
                            id=additional_field_id,
                            defaults={
                                'name_uk': name,
                                'value_uk': value,
                                'product_id': product_id
                            }
                        )
                    else:
                        self.stdout.write(self.style.WARNING(f'Product ID {product_id} does not exist. Skipping additional field.'))
        self.stdout.write(self.style.SUCCESS('Successfully imported additional fields from additional_fields.csv'))
