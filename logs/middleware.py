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
        some_seconds_ago = timezone.now() - timezone.timedelta(seconds=10)
        
        # Only log Android WebView requests (always)
        if self.is_android_webview_request(request):
            self.log_android_request(endpoint, current_timestamp)
        else:
            # Log Vercel (non-Android) requests only if not already logged in the last 10 seconds
            if not self.is_duplicate_request(endpoint, some_seconds_ago):
                self.log_non_android_request(endpoint, current_timestamp)

        return None

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def is_android_webview_request(self, request):
        return request.headers.get('X-Android-Client') == 'Koloryt'

    def is_duplicate_request(self, endpoint, some_seconds_ago):
        recent_requests = APILog.objects.filter(endpoint=endpoint, timestamp__gte=some_seconds_ago)
        return recent_requests.exists()

    def log_android_request(self, endpoint, current_timestamp):
        endpoint = self.clean_endpoint(endpoint)
        log_entry = APILog.objects.create(
            endpoint=endpoint,
            request_count=1,
            timestamp=current_timestamp,
        )
        logger.info(f"Logged Android WebView request: endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")

    def log_non_android_request(self, endpoint, current_timestamp):
        endpoint = self.clean_endpoint(endpoint)
        log_entry = APILog.objects.create(
            endpoint=endpoint,
            request_count=1,
            timestamp=current_timestamp,
        )
        logger.info(f"Logged non-Android request: endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")

    def clean_endpoint(self, endpoint):
        return endpoint.replace('http://', '')
