from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog, IgnoreEndpoint, APILogExcluded
from urllib.parse import unquote
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    CACHE_TIMEOUT = 10  # Cache duration in seconds for duplicate request checks

    def process_request(self, request):
        current_timestamp = timezone.localtime(timezone.now()).replace(second=0, microsecond=0)
        endpoint = unquote(request.build_absolute_uri())
        cache_key = f"api_log:{endpoint}:{current_timestamp}"
        is_android = self.is_android_webview_request(request)

        if is_android:
            endpoint = endpoint.replace('https://', '')

        if self.should_exclude_request(request):
            return None

        # Check for duplicates
        if not cache.get(cache_key):
            is_vercel = self.is_vercel_request(request)
            ignore_endpoint = IgnoreEndpoint.objects.filter(name__icontains=request.path, is_active=True).first()
            if ignore_endpoint:
                self.handle_excluded_log(endpoint, current_timestamp, is_android, is_vercel)
            else:
                self.log_request(endpoint, current_timestamp, is_android, is_vercel)

            cache.set(cache_key, True, self.CACHE_TIMEOUT)
        return None

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def should_exclude_request(self, request):
        host = request.get_host()
        excluded_domains = ['myshop-six-wheat'] 
        return any(excluded_domain in host for excluded_domain in excluded_domains)

    def is_android_webview_request(self, request):
        return request.headers.get('X-Android-Client', '').lower() == 'koloryt'

    def is_vercel_request(self, request):
        return request.META.get('SERVER_NAME', '').endswith('.vercel.app')

    def log_request(self, endpoint, current_timestamp, is_android, is_vercel):
        log_entry = APILog.objects.create(
            endpoint=endpoint,
            timestamp=current_timestamp,
        )
        log_type = "Android WebView" if is_android else "Vercel" if is_vercel else "Other"
        logger.info(f"Logged {log_type} request: endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")

    def handle_excluded_log(self, endpoint, current_timestamp, is_android, is_vercel):
        # Log excluded requests to APILogExcluded
        excluded_log_entry = APILogExcluded.objects.create(
            endpoint=endpoint,
            timestamp=current_timestamp,
        )
        logger.info(f"Excluded request moved to APILogExcluded: endpoint={endpoint}, Timestamp={excluded_log_entry.timestamp}")
