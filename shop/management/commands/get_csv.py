import csv
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Export data from the database to CSV files'

    def handle(self, *args, **options):
        self.export_products()
        self.export_categories()
        self.export_collections()
        self.export_additional_fields()

    def export_categories(self):
        with open('categories.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['id', 'name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            query = '''
                SELECT id, name
                FROM shop_category
            '''
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    writer.writerow({
                        'id': row[0],
                        'name': row[1]
                    })

        self.stdout.write(self.style.SUCCESS('Successfully exported categories to categories.csv'))

    def export_collections(self):
        with open('collections.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['id', 'name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            query = '''
                SELECT id, name
                FROM shop_collection
            '''
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    writer.writerow({
                        'id': row[0],
                        'name': row[1]
                    })

        self.stdout.write(self.style.SUCCESS('Successfully exported collections to collections.csv'))

    def export_products(self):
        with open('products.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['id', 'name', 'description', 'color_name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            query = '''
                SELECT id, name, description, color_name
                FROM shop_product
            '''
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    writer.writerow({
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'color_name': row[3]  # Ensure color_name is included
                    })

        self.stdout.write(self.style.SUCCESS('Successfully exported products to products.csv'))

    def export_additional_fields(self):
        with open('additional_fields.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['id', 'name', 'value', 'product_id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            query = '''
                SELECT id, name, value, product_id
                FROM shop_additionalfield
            '''
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    writer.writerow({
                        'id': row[0],
                        'name': row[1],
                        'value': row[2],
                        'product_id': row[3]
                    })

        self.stdout.write(self.style.SUCCESS('Successfully exported additional fields to additional_fields.csv'))
