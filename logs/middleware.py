from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get the current timestamp at the start of request processing
        current_timestamp = timezone.localtime(timezone.now())
        # Round timestamp to the nearest second (ignore microseconds)
        rounded_timestamp = current_timestamp.replace(microsecond=0)
        # Determine the endpoint
        endpoint = unquote(request.path)
        # Check if there is an existing log entry for the same endpoint at the same rounded timestamp
        existing_log = APILog.objects.filter(endpoint=endpoint, timestamp=rounded_timestamp).exists()

        # Handle endpoint processing based on the type of request
        if self.is_android_request(request):
            # Remove the "https://" part for Android requests
            host = request.get_host().replace('https://', '').replace('http://', '')
            endpoint = f"{host}{endpoint}"
            logger.debug(f"Logging Android request for endpoint: {endpoint}")

        elif self.is_internal_request(request):
            # Handle internal requests
            host = request.get_host()
            endpoint = f"{host}{endpoint}"
        
        elif self.is_vercel_request(request) and self.is_android_request(request):
            # Remove "https://" part for Vercel requests caused by Android headers
            host = request.get_host().replace('https://', '').replace('http://', '')
            endpoint = f"{host}{endpoint}"
            logger.debug(f"Vercel Android request for endpoint: {endpoint}")

        else:
            # For other requests, log the full absolute URI
            endpoint = unquote(request.build_absolute_uri())

        # Log only if there's no existing log for the same endpoint and timestamp
        if not existing_log:
            log_entry = APILog.objects.create(
                endpoint=endpoint,
                request_count=1,  # Always set request_count to 1 for each request
                timestamp=rounded_timestamp  # Store the rounded timestamp (no microseconds)
            )
            logger.info(f"Logged request: Endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
        else:
            logger.debug(f"Duplicate request detected for {endpoint} at timestamp {rounded_timestamp}. Skipping duplicate logging.")

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def is_internal_request(self, request):
        host = request.get_host()
        internal_hosts = [
            "localhost:8000",
            "127.0.0.1:8000",
            "localhost:8010",
            "127.0.0.1:8010"
        ]
        return any(host == internal_host or host.endswith(f".{internal_host}") for internal_host in internal_hosts)
    
    def is_vercel_request(self, request):
        host = request.get_host()
        return hasattr(settings, "VERCEL_DOMAIN") and host in settings.VERCEL_DOMAIN

    def is_android_request(self, request):
        return request.headers.get('X-Android-Client') == 'Koloryt'
