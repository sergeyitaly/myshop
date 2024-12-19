from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        endpoint = unquote(request.path)

        # Check if the request is coming from the Android app
        if self.is_android_request(request):
            host = request.get_host()
            endpoint = f"{host}{endpoint}"
            logger.debug(f"Logging Android request for endpoint: {endpoint}")
        elif self.is_internal_request(request):
            # Handle internal requests differently if needed
            host = request.get_host()
            endpoint = f"{host}{endpoint}"
        else:
            endpoint = unquote(request.build_absolute_uri())

        log_entry = APILog.objects.create(
            endpoint=endpoint,
            request_count=1,  # Start with count = 1 for each request
            timestamp=timezone.localtime(timezone.now())  # Store the exact timestamp
        )

        logger.info(f"Logged request: Endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")

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
