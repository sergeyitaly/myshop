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
        some_seconds_ago = current_timestamp - timezone.timedelta(seconds=10)
        if self.should_log_request(request, endpoint):
            self.log_request(endpoint, current_timestamp=current_timestamp, some_seconds_ago=some_seconds_ago)
        return None

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def should_log_request(self, request, endpoint):
        is_android_webview = (
            "https://" not in endpoint
            and request.headers.get('X-Android-Client') == 'Koloryt'
        )
        is_vercel_request = (
            "https://" in endpoint
            and request.META.get('SERVER_NAME', '').endswith('.vercel.app')
            and request.is_secure()
        )
        is_local_request = (
            "http://" in endpoint
        )
        return is_android_webview or is_vercel_request or is_local_request

    def log_request(self, endpoint, current_timestamp, some_seconds_ago):

        endpoint = endpoint.replace('http://', '').strip()
        endpoint_for_duplicate = endpoint.replace('https://', '').strip()
        duplicate = APILog.objects.filter(endpoint=endpoint_for_duplicate, timestamp__gte=some_seconds_ago).exists()
        if not duplicate:
            log_entry = APILog.objects.create(
                endpoint=endpoint,
                request_count=1,
                timestamp=current_timestamp,
            )
            logger.info(f"Logged endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
        else:
            logger.debug(f"Duplicate detected for {endpoint}. Skipping log.")
