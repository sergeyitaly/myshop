import os
import redis
import psycopg2
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from urllib.parse import urlparse

class Command(BaseCommand):
    help = 'Connects to Redis and Supabase PostgreSQL database'

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

        redis_password = url.password  # Get the password from the URL
        redis_host = url.hostname  # Get the host from the URL
        redis_port = url.port  # Get the port from the URL

        # Connect to PostgreSQL
        try:
            connection = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            self.stdout.write(self.style.SUCCESS('Successfully connected to Supabase PostgreSQL'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to connect to Supabase PostgreSQL: {e}'))

        # Connect to Redis
        try:
            redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                decode_responses=True
            )
            # Test the connection
            redis_client.ping()
            self.stdout.write(self.style.SUCCESS('Successfully connected to Redis'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to connect to Redis: {e}'))
