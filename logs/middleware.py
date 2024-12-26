from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote
import logging

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_timestamp = timezone.localtime(timezone.now()).replace(second=0, microsecond=0)
        endpoint = unquote(request.build_absolute_uri())
        cleaned_endpoint = endpoint.replace('http://', '')
        some_seconds_ago = timezone.now() - timezone.timedelta(seconds=10)
        self.log_request(cleaned_endpoint, current_timestamp, some_seconds_ago)
        return None

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def is_android_webview_request(self, request, endpoint):
        return "https://" not in endpoint and request.headers.get('X-Android-Client') == 'Koloryt'

    def is_vercel_production_request(self, request, endpoint):
        return "https://" in endpoint and request.META.get('SERVER_NAME', '').endswith('.vercel.app') and request.is_secure()

    def log_request(self, endpoint, current_timestamp, some_seconds_ago):
        duplicate = APILog.objects.filter(endpoint=endpoint, timestamp__gte=some_seconds_ago)

        if not duplicate.exists() and self.is_vercel_production_request:
            log_entry = APILog.objects.create(
                endpoint=endpoint.replace('https://', ''),
                request_count=1,
                timestamp=current_timestamp,
            )
            logger.info(f"Logged endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
        elif not duplicate.exists() and self.is_android_webview_request:
            log_entry = APILog.objects.create(
                endpoint=endpoint.replace('https://', ''),
                request_count=1,
                timestamp=current_timestamp,
            )
            logger.info(f"Logged endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
        elif not duplicate.exists():
            log_entry = APILog.objects.create(
                endpoint=endpoint,
                request_count=1,
                timestamp=current_timestamp,
            )
            logger.info(f"Logged endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")        
        
        else:
            logger.debug(f"Duplicate request detected for {endpoint}. Skipping log.")
