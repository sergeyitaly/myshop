from django.core.management.base import BaseCommand
from django.urls import get_resolver
from logs.models import APILog
from datetime import datetime

class Command(BaseCommand):
    help = "Logs visit counts of available endpoints, excluding specified ones."

    excluded_endpoints = {
        'redis_performance', 
        'database_performance', 
        'token_obtain_pair', 
        'token_refresh'
    }

    def handle(self, *args, **kwargs):
        url_patterns = get_resolver().url_patterns
        for url_pattern in url_patterns:
            self._log_endpoint(url_pattern)
        self.stdout.write(self.style.SUCCESS('Successfully counted visits for all endpoints!'))

    def _log_endpoint(self, url_pattern):
        if hasattr(url_pattern, 'url_patterns'):  # Handle nested URLs
            for nested_url in url_pattern.url_patterns:
                self._log_endpoint(nested_url)
        else:
            endpoint = str(url_pattern.pattern)
            endpoint_name = getattr(url_pattern, 'name', None)
            
            if endpoint_name in self.excluded_endpoints:
                return  # Skip this endpoint

            # Determine if endpoint includes 'chat_id'
            has_chat_id = 'chat_id' in endpoint

            # Update or create a log entry for the endpoint
            log, created = APILog.objects.get_or_create(
                endpoint=endpoint,
                defaults={'get_count': 0, 'post_count': 0, 'has_chat_id': has_chat_id},
            )

            # Ensure `has_chat_id` is correctly set for existing entries
            if not created and log.has_chat_id != has_chat_id:
                log.has_chat_id = has_chat_id
                log.save()