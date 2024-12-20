from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        raw_endpoint = unquote(request.build_absolute_uri())
        normalized_endpoint = self.normalize_endpoint(raw_endpoint)
        
        if self.is_duplicate_request(normalized_endpoint):
            logger.debug(f"Skipping duplicate request for endpoint: {normalized_endpoint}")
            return  # Skip processing for duplicates
        endpoint = self.get_full_endpoint(request, normalized_endpoint)
        
        log_entry = APILog.objects.create(
            endpoint=endpoint,
            request_count=1,
            timestamp=timezone.localtime(timezone.now())
        )
        logger.info(f"Logged request: Endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def normalize_endpoint(self, raw_endpoint):
        if raw_endpoint.startswith('https://'):
            return raw_endpoint.replace('https://', '', 1)
        if raw_endpoint.startswith('http://'):
            return raw_endpoint.replace('http://', '', 1)
        return raw_endpoint

    def get_full_endpoint(self, request, normalized_endpoint):
        if self.is_internal_request(request):
            host = request.get_host()
            return f"{host}{normalized_endpoint}"
        else:
            vercel_domain = getattr(settings, "VERCEL_DOMAIN", "")
            return f"{vercel_domain}{normalized_endpoint}" if vercel_domain else normalized_endpoint

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

    def is_duplicate_request(self, normalized_endpoint):
        if not hasattr(self, 'processed_endpoints'):
            self.processed_endpoints = set()  # Keep track of processed endpoints
        
        if normalized_endpoint in self.processed_endpoints:
            return True  # Duplicate request
        self.processed_endpoints.add(normalized_endpoint)  # Mark as processed
        return False
