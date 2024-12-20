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
        rounded_timestamp = current_timestamp.replace(microsecond=1000)
        # Determine the endpoint
        endpoint = unquote(request.path)
        # Check if the request contains the Android header
        is_android_request = self.is_android_request(request)

        # Check if this timestamp has any Android request logged
        if is_android_request:
            # If this request has the Android header, remove the https:// or http:// from all requests
            host = request.get_host().replace('https://', '').replace('http://', '')
            endpoint = f"{host}{endpoint}"
            logger.debug(f"Android request detected. Stripping https:// from endpoint: {endpoint}")
        else:
            # For non-Android requests, log normally
            host = request.get_host()
            endpoint = f"{host}{endpoint}"

        # Check if there is an existing log entry for the same endpoint at the same timestamp
        existing_log = APILog.objects.filter(endpoint=endpoint, timestamp=rounded_timestamp).first()

        if not existing_log:
            # Log the request only if there is no existing log entry for the same endpoint at the same timestamp
            log_entry = APILog.objects.create(
                endpoint=endpoint,
                request_count=1,  # Always set request_count to 1 for each request
                timestamp=rounded_timestamp  # Store the rounded timestamp (no microseconds)
            )

            logger.info(f"Logged request: Endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
        else:
            # If the log entry already exists, do nothing (no duplication)
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
        if hasattr(settings, "VERCEL_DOMAIN"):
            internal_hosts.append(settings.VERCEL_DOMAIN)
        return any(host == internal_host or host.endswith(f".{internal_host}") for internal_host in internal_hosts)

    def is_android_request(self, request):
        return request.headers.get('X-Android-Client') == 'Koloryt'
