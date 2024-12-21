from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_timestamp = timezone.localtime(timezone.now()).replace(microsecond=0)
        is_android = self.is_android_request(request)
        is_vercel = self.is_vercel_request(request)
        endpoint = urlparse(request.build_absolute_uri()).path
        if is_vercel and is_android:
            endpoint = endpoint.replace('https://', '', 1)
            logger.debug(f"Modified endpoint for Vercel Android WebView: {endpoint}")
        if is_vercel and self.is_android_origin(request):
            logger.debug(f"Skipping Vercel request for endpoint {endpoint} since it's caused by Android WebView.")
            return
        time_window_start = current_timestamp - timezone.timedelta(seconds=7)
        existing_log = APILog.objects.filter(
            endpoint=endpoint,
            timestamp__gte=time_window_start,
            timestamp__lte=current_timestamp
        ).exists()
        if not existing_log:
            log_entry = APILog.objects.create(
                endpoint=endpoint,
                request_count=1,
                timestamp=current_timestamp
            )
            logger.info(f"Logged request: Endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
        else:
            logger.debug(f"Duplicate request detected for {endpoint} at {current_timestamp}. Skipping duplicate logging.")

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def is_android_request(self, request):
        if request.headers.get('X-Android-Client') == 'Koloryt':
            return True
        user_agent = request.headers.get('User-Agent', '').lower()
        if "android" in user_agent and "webview" in user_agent:
            return True
        return False

    def is_vercel_request(self, request):
        if request.headers.get('X-Vercel-Client'):
            return True
        return request.META.get('SERVER_NAME', '').endswith('.vercel.app')

    def is_android_origin(self, request):
        return request.headers.get('X-Android-Origin') == 'True'
