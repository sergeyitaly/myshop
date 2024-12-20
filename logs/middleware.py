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
        normalized_endpoint = endpoint.replace('https://', '')  # Remove https:// for Android WebView requests
        if self.is_duplicate_request_with_https(endpoint, normalized_endpoint):
            logger.debug(f"Skipping duplicate request with 'https://' for endpoint: {endpoint}")
            return
        if self.is_internal_request(request):
            host = request.get_host()
            endpoint = f"{host}{normalized_endpoint}"  # Append host for internal requests
        else:
            vercel_domain = getattr(settings, "VERCEL_DOMAIN", "")
            endpoint = f"{vercel_domain}{normalized_endpoint}" if vercel_domain else normalized_endpoint
        log_entry = APILog.objects.create(
            endpoint=endpoint,
            request_count=1,
            timestamp=timezone.localtime(timezone.now())
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

    def is_duplicate_request_with_https(self, endpoint, normalized_endpoint):
        if not hasattr(self, 'processed_urls_https'):
            self.processed_urls_https = set()
        if endpoint.startswith('https://') and normalized_endpoint in self.processed_urls_https:
            return True
        if endpoint.startswith('https://'):
            self.processed_urls_https.add(normalized_endpoint)

        return False
