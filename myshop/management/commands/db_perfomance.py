# myshop/management/commands/check_performance.py

import os
import time
import requests
from django.core.management.base import BaseCommand
from django.urls import get_resolver

class Command(BaseCommand):
    help = 'Check the performance of all endpoints.'

    def handle(self, *args, **options):
        # Get the Vercel domain from environment variables
        base_url = os.environ.get('VERCEL_DOMAIN')
        
        if not base_url:
            self.stdout.write(self.style.ERROR('VERCEL_DOMAIN not found in environment variables.'))
            return
        
        # Gather all URL patterns
        urlconf = get_resolver().urlconf_name
        urlpatterns = get_resolver(urlconf).url_patterns
        endpoints = [pattern for pattern in urlpatterns if hasattr(pattern, 'name')]

        for endpoint in endpoints:
            endpoint_name = endpoint.name
            # Ensure there's a trailing slash on the base_url if it's not already present
            if not base_url.endswith('/'):
                base_url += '/'
            # Construct the full URL for the endpoint
            endpoint_url = f"{base_url}{endpoint.pattern}"
            self.check_endpoint(endpoint_name, endpoint_url)

    def check_endpoint(self, name, url):
        start_time = time.time()
        try:
            response = requests.get(url)
            duration = time.time() - start_time
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS(f"{name} executed successfully. Duration: {duration:.2f} seconds."))
            else:
                self.stdout.write(self.style.WARNING(f"{name} failed with status {response.status_code}."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error executing {name}: {str(e)}"))
