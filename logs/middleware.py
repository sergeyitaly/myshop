# middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote
import logging

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        endpoint = unquote(request.path)
        
        host = request.get_host()
        if host in request.META['HTTP_HOST']: 
            # If internal, save only the path (no domain)
            endpoint = endpoint
        else:
            # If external, save the full URL
            endpoint = request.build_absolute_uri()
        
        logger.debug(f"Logging request for endpoint: {endpoint}")
        
        # Create a new log entry for the endpoint
        log_entry = APILog.objects.create(
            endpoint=endpoint,
            request_count=1,  # Start with count = 1 for each request
            timestamp=timezone.localtime(timezone.now())  # Store the exact timestamp
        )
        
        logger.info(f"Logged new request: Endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response
