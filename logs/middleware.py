from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
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

        if not cache.get(cache_key):
            is_android = self.is_android_webview_request(request)
            is_vercel = self.is_vercel_request(request)
            self.log_request(endpoint, current_timestamp, is_android, is_vercel)
            cache.set(cache_key, True, self.CACHE_TIMEOUT)

        return None

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def is_android_webview_request(self, request):
        return request.headers.get('X-Android-Client', '').lower() == 'koloryt'

    def is_vercel_request(self, request):
        return 'x-vercel-id' in request.headers

    def log_request(self, endpoint, current_timestamp, is_android, is_vercel):
        log_entry = APILog.objects.create(
            endpoint=endpoint,
            timestamp=current_timestamp,
        )
        if is_android:
            log_type = "Android WebView"
        elif is_vercel:
            log_type = "Vercel"
        else:
            log_type = "Other"
        
        logger.info(f"Logged {log_type} request: endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
