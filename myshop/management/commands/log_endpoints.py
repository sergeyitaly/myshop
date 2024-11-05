from django.core.management.base import BaseCommand
from django.urls import get_resolver
from logs.models import APILog  # Assuming your log model is named APILog
from datetime import datetime

class Command(BaseCommand):
    help = "Logs all available endpoints in the system, excluding specified ones"

    excluded_endpoints = {
        'redis_performance', 
        'database_performance', 
        'token_obtain_pair', 
        'token_refresh'
    }

    def handle(self, *args, **kwargs):
        # Get all URL patterns
        url_patterns = get_resolver().url_patterns

        # Loop through the URL patterns and log each endpoint
        for url_pattern in url_patterns:
            self._log_endpoint(url_pattern)

        self.stdout.write(self.style.SUCCESS('Successfully logged all endpoints!'))

    def _log_endpoint(self, url_pattern):
        """
        Logs a single URL pattern into the APILog model, if it's not in the excluded endpoints.
        """
        if hasattr(url_pattern, 'url_patterns'):  # This is a nested include
            for nested_url in url_pattern.url_patterns:
                self._log_endpoint(nested_url)
        else:
            # Here we handle the individual path
            endpoint = str(url_pattern.pattern)
            endpoint_name = getattr(url_pattern, 'name', None)  # Get the name attribute if available

            # Check if the endpoint is in the excluded list
            if endpoint_name in self.excluded_endpoints:
                return  # Skip logging this endpoint

            # Create a new log entry for this endpoint
            APILog.objects.create(
                timestamp=datetime.now(),
                source='system',
                endpoint=endpoint,
                method='GET',  # You can modify this based on the HTTP methods supported
#                chat_id=None,  # Optional field
                command='Log endpoint',  # You can customize this
            )
