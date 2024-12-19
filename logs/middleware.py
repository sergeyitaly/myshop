from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote, urlparse
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        endpoint = unquote(request.path)
        if not self.is_internal_request(request):
            endpoint = unquote(request.build_absolute_uri())
        else:
            endpoint = endpoint
        logger.debug(f"Logging request for endpoint: {endpoint}")
        log_entry = APILog.objects.create(
            endpoint=endpoint,
            request_count=1,  # Start with count = 1 for each request
            timestamp=timezone.localtime(timezone.now())  # Store the exact timestamp
        )

        logger.info(f"Logged new request: Endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def is_internal_request(self, request):
        host = request.get_host()
        return host
#        return host == "localhost:8000" or "127.0.0.1:8000" or host.endswith(settings.VERCEL_DOMAIN)

