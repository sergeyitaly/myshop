import os
import time
import requests
from django.core.management.base import BaseCommand
from django.urls import get_resolver, include, URLPattern, URLResolver

class Command(BaseCommand):
    help = 'Check the performance of all endpoints, excluding certain ones.'

    def handle(self, *args, **options):
        # Get the Vercel domain from environment variables
        base_url = os.environ.get('VERCEL_DOMAIN')
        
        if not base_url:
            self.stdout.write(self.style.ERROR('VERCEL_DOMAIN not found in environment variables.'))
            return
        
        # Gather all URL patterns
        urlconf = get_resolver().urlconf_name
        urlpatterns = get_resolver(urlconf).url_patterns
        
        # Exclude specific endpoints
        excluded_endpoints = {
            'redis_performance', 
            'database_performance', 
            'token_obtain_pair', 
            'token_refresh'
        }

        endpoints = []
        self.collect_endpoints(urlpatterns, base_url, endpoints, excluded_endpoints)

        for endpoint in endpoints:
            endpoint_name = endpoint.name if endpoint.name else str(endpoint.pattern)
            endpoint_url = f"{base_url}{endpoint.pattern}"
            self.check_endpoint(endpoint_name, endpoint_url)

    def collect_endpoints(self, urlpatterns, base_url, endpoints, excluded_endpoints):
        for pattern in urlpatterns:
            if isinstance(pattern, URLPattern):
                if pattern.name and pattern.name not in excluded_endpoints:
                    endpoints.append(pattern)
            elif isinstance(pattern, URLResolver):
                # Recur into nested URLResolvers
                self.collect_endpoints(pattern.url_patterns, base_url, endpoints, excluded_endpoints)

    def check_endpoint(self, name, url):
        start_time = time.time()
        try:
            response = requests.get(url)
            duration = time.time() - start_time
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS(f"{name} executed successfully. Duration: {duration:.2f} seconds."))
            # You can optionally handle other status codes here if needed
        except Exception as e:
            # Optionally log the error to console or log file if necessary
            pass  # Do nothing on exception, effectively dropping the error message
