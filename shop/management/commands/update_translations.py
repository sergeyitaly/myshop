import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from shop.models import Product, Category, Collection, AdditionalField
from modeltranslation.translator import translator

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Command(BaseCommand):
    help = 'Copy values from non-translated fields to translated fields'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.copy_product_translations()
            self.copy_category_translations()
            self.copy_collection_translations()
            self.copy_additional_field_translations()

    def copy_product_translations(self):
        products = Product.objects.all()
        updated_count = 0
        for product in products:
            fields_to_update = {}
            if not product.name_en and product.name:
                fields_to_update['name_en'] = product.name
            if not product.name_uk and product.name:
                fields_to_update['name_uk'] = product.name
            if not product.description_en and product.description:
                fields_to_update['description_en'] = product.description
            if not product.description_uk and product.description:
                fields_to_update['description_uk'] = product.description
            if not product.color_value_en and product.color_value:
                fields_to_update['color_value_en'] = product.color_value
            if not product.color_value_uk and product.color_value:
                fields_to_update['color_value_uk'] = product.color_value
            
            if fields_to_update:
                for field, value in fields_to_update.items():
                    setattr(product, field, value)
                product.save()
                updated_count += 1
        logger.info(f'Successfully updated {updated_count} Product translations')
        self.stdout.write(self.style.SUCCESS(f'Successfully updated Product translations'))

    def copy_category_translations(self):
        categories = Category.objects.all()
        updated_count = 0
        for category in categories:
            fields_to_update = {}
            if not category.name_en and category.name:
                fields_to_update['name_en'] = category.name
            if not category.name_uk and category.name:
                fields_to_update['name_uk'] = category.name
            
            if fields_to_update:
                for field, value in fields_to_update.items():
                    setattr(category, field, value)
                category.save()
                updated_count += 1
        logger.info(f'Successfully updated {updated_count} Category translations')
        self.stdout.write(self.style.SUCCESS(f'Successfully updated Category translations'))

    def copy_collection_translations(self):
        collections = Collection.objects.all()
        updated_count = 0
        for collection in collections:
            fields_to_update = {}
            if not collection.name_en and collection.name:
                fields_to_update['name_en'] = collection.name
            if not collection.name_uk and collection.name:
                fields_to_update['name_uk'] = collection.name
            
            if fields_to_update:
                for field, value in fields_to_update.items():
                    setattr(collection, field, value)
                collection.save()
                updated_count += 1
        logger.info(f'Successfully updated {updated_count} Collection translations')
        self.stdout.write(self.style.SUCCESS(f'Successfully updated Collection translations'))

    def copy_additional_field_translations(self):
        additional_fields = AdditionalField.objects.all()
        updated_count = 0
        for field in additional_fields:
            fields_to_update = {}
            if not field.name_en and field.name:
                fields_to_update['name_en'] = field.name
            if not field.name_uk and field.name:
                fields_to_update['name_uk'] = field.name
            if not field.value_en and field.value:
                fields_to_update['value_en'] = field.value
            if not field.value_uk and field.value:
                fields_to_update['value_uk'] = field.value
            
            if fields_to_update:
                for field_name, value in fields_to_update.items():
                    setattr(field, field_name, value)
                field.save()
                updated_count += 1
        logger.info(f'Successfully updated {updated_count} AdditionalField translations')
        self.stdout.write(self.style.SUCCESS(f'Successfully updated AdditionalField translations'))
