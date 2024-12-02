import os
import redis
import psycopg2
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from urllib.parse import urlparse
import json
from decimal import Decimal
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class Command(BaseCommand):
    help = 'Connects to Redis and Supabase PostgreSQL database and caches all data from PostgreSQL in Redis'

    def handle(self, *args, **kwargs):
        # Load environment variables from .env file
        load_dotenv()

        # PostgreSQL connection details
        db_name = os.getenv('POSTGRES_DATABASE')
        db_user = os.getenv('POSTGRES_USER')
        db_password = os.getenv('POSTGRES_PASSWORD')
        db_host = os.getenv('POSTGRES_HOST')
        db_port = os.getenv('POSTGRES_PORT')

        # Redis connection details
        redis_cache_location = os.getenv('REDIS_CACHE_LOCATION')

        if not redis_cache_location:
            self.stdout.write(self.style.ERROR('REDIS_CACHE_LOCATION is not set in the environment variables.'))
            return

        # Parse the REDIS_CACHE_LOCATION to get Redis connection details
        url = urlparse(redis_cache_location)
        redis_password = url.password
        redis_host = url.hostname
        redis_port = url.port
        redis_db = int(url.path[1:]) if url.path else 0

        # Connect to PostgreSQL
        try:
            connection = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            cursor = connection.cursor()
            self.stdout.write(self.style.SUCCESS('Successfully connected to Supabase PostgreSQL'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to connect to Supabase PostgreSQL: {e}'))
            return

        # Connect to Redis
        try:
            redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                db=redis_db,
                decode_responses=True
            )
            redis_client.ping()
            self.stdout.write(self.style.SUCCESS(f'Successfully connected to Redis on database {redis_db}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to connect to Redis: {e}'))
            return

        # Fetch and cache data from all tables in PostgreSQL
        try:
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public';
            """)
            tables = cursor.fetchall()

            # Use ThreadPoolExecutor for parallel processing
            with ThreadPoolExecutor() as executor:
                for table in tables:
                    executor.submit(self.cache_table_data, cursor, redis_client, table[0])

            self.stdout.write(self.style.SUCCESS("Successfully cached all data from the database in Redis."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to fetch or cache data: {e}"))
        finally:
            # Close the PostgreSQL cursor and connection
            cursor.close()
            connection.close()
            self.stdout.write(self.style.SUCCESS("Closed PostgreSQL connection."))

    def cache_table_data(self, cursor, redis_client, table_name):
        try:
            self.stdout.write(self.style.SUCCESS(f'Caching data from table: {table_name}'))

            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            # Use Redis pipeline to batch commands
            pipeline = redis_client.pipeline()
            batch_size = 100  # Number of commands per batch
            batch_count = 0  # Counter for batching commands

            for row in rows:
                row_data = dict(zip(columns, row))

                # Convert Decimal and datetime fields
                for key, value in row_data.items():
                    if isinstance(value, Decimal):
                        row_data[key] = float(value)
                    elif isinstance(value, datetime):
                        row_data[key] = value.isoformat()

                item_id = row_data.get('id')
                if item_id:
                    redis_key = f"{table_name}:{item_id}"

                    # Check if the key exists before setting
                    if not redis_client.exists(redis_key):
                        pipeline.set(redis_key, json.dumps(row_data))
                        batch_count += 1

                        # Execute pipeline in batches
                        if batch_count >= batch_size:
                            pipeline.execute()  # Execute the batch
                            batch_count = 0
                            pipeline = redis_client.pipeline()  # Reset the pipeline

            # Final execution for remaining items if any
            if batch_count > 0:
                pipeline.execute()

            self.stdout.write(self.style.SUCCESS(f"Successfully cached data from table {table_name} in Redis."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to cache data from table {table_name}: {e}"))
