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
        is_android_webview = self.is_android_webview_request(request)
        is_vercel_production = self.is_vercel_production_request(request)
        cleaned_endpoint = endpoint.replace('http://', '').replace('https://', '')
        some_seconds_ago = timezone.now() - timezone.timedelta(seconds=10)
        duplicate = APILog.objects.filter(endpoint=cleaned_endpoint, timestamp__gte=some_seconds_ago).first()

        if is_android_webview:
            if duplicate:
                logger.debug(f"Duplicate Android WebView request detected for {cleaned_endpoint}. Skipping log.")
                return None
            log_entry = APILog.objects.create(
                endpoint=cleaned_endpoint,
                request_count=1,
                timestamp=current_timestamp
            )
            logger.info(f"Logged Android WebView request: Endpoint={cleaned_endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
            return None

        if is_vercel_production:
            if duplicate:
                logger.debug(f"Duplicate Vercel request detected for {cleaned_endpoint}. Skipping log.")
                return None
            log_entry = APILog.objects.create(
                endpoint=endpoint,  # Keep original endpoint with https:// for Vercel logs
                request_count=1,
                timestamp=current_timestamp
            )
            logger.info(f"Logged Vercel request: Endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
            return None

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def is_android_webview_request(self, request):
        if request.headers.get('X-Android-Client') == 'Koloryt':
            return True
        user_agent = request.headers.get('User-Agent', '').lower()
        if "android" in user_agent and "webview" in user_agent:
            return True
        return False

    def is_vercel_production_request(self, request):
        return (
            request.META.get('SERVER_NAME', '').endswith('.vercel.app')
            and request.is_secure()  # Ensures the request is over HTTPS
        )
