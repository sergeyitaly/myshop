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
        cleaned_endpoint = endpoint.replace('http://', '').replace('https://', '')
        some_seconds_ago = timezone.now() - timezone.timedelta(seconds=10)
        is_android_webview = self.is_android_webview_request(request, endpoint)
        if is_android_webview:
            self.log_request(cleaned_endpoint, 'Android', current_timestamp, some_seconds_ago)
            return None
        is_vercel_production = self.is_vercel_production_request(request)
        if is_vercel_production:
            self.log_request(endpoint, 'Vercel', current_timestamp, some_seconds_ago)
            return None
        self.log_request(cleaned_endpoint, 'Local', current_timestamp, some_seconds_ago)

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def is_android_webview_request(self, request, endpoint):
        if request.headers.get('X-Android-Client') == 'Koloryt':
            return True
        if "https://" not in endpoint:
            return True
        return False

    def is_vercel_production_request(self, request):
        return (
            request.META.get('SERVER_NAME', '').endswith('.vercel.app')
            and request.is_secure()  # Ensures the request is over HTTPS
        )

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
