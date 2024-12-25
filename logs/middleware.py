from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote
import logging

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_timestamp = timezone.localtime(timezone.now()).replace(second=0, microsecond=0)
        endpoint = unquote(request.build_absolute_uri()).replace('https://', '')
        some_seconds_ago = timezone.now() - timezone.timedelta(seconds=10)
        if self.is_android_webview_request(request, endpoint):
            cleaned_endpoint = self.clean_endpoint(endpoint, is_webview=True)
            self.log_request(cleaned_endpoint, 'Android WebView', current_timestamp, some_seconds_ago)
            return None
        if self.is_vercel_production_request(request, endpoint):
            cleaned_endpoint = self.clean_endpoint(endpoint, is_webview=False)
            self.log_request(cleaned_endpoint, 'Vercel', current_timestamp, some_seconds_ago)
            return None
        self.log_request(cleaned_endpoint, 'LOcalhost', current_timestamp, some_seconds_ago)
        return None

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def is_android_webview_request(self, request, endpoint):
        return "https://" not in endpoint and request.headers.get('X-Android-Client') == 'Koloryt'

    def is_vercel_production_request(self, request, endpoint):
        return "https://" in endpoint and request.META.get('SERVER_NAME', '').endswith('.vercel.app') and request.is_secure()

    def clean_endpoint(self, endpoint, is_webview):
        if is_webview:
            return endpoint.replace('https://', '').strip()
        else:
            return endpoint.strip()

    def log_request(self, endpoint, request_type, current_timestamp, some_seconds_ago):
        duplicate = APILog.objects.filter(endpoint=endpoint, timestamp__gte=some_seconds_ago)

        if not duplicate.exists():
            log_entry = APILog.objects.create(
                endpoint=endpoint,
                request_count=1,
                timestamp=current_timestamp,
            )
            logger.info(f"Logged {request_type} request: Endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
        else:
            logger.debug(f"Duplicate {request_type} request detected for {endpoint}. Skipping log.")
