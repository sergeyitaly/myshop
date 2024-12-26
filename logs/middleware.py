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
        endpoint = endpoint.replace("http://", "")

        some_seconds_ago = current_timestamp - timezone.timedelta(seconds=10)
        is_android_webview = (
            request.headers.get('X-Android-Client', '').lower() == 'koloryt'
        )
        is_vercel_request = (
            request.META.get('SERVER_NAME', '').endswith('.vercel.app')
            )
        is_local_request = "http://" in endpoint

        logger.debug(
            f"Processing request: {endpoint}, "
            f"is_android_webview={is_android_webview}, "
            f"is_vercel_request={is_vercel_request}, "
            f"is_local_request={is_local_request}"
        )
        logger.debug(f"Headers: {request.headers}")
        if is_android_webview or is_vercel_request or is_local_request:
            self.log_request(
                endpoint,
                current_timestamp=current_timestamp,
                some_seconds_ago=some_seconds_ago,
                is_android_webview=is_android_webview,
                is_vercel_request=is_vercel_request
            )

        return None

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def log_request(self, endpoint, current_timestamp, some_seconds_ago, is_android_webview, is_vercel_request):
        duplicates = APILog.objects.filter(endpoint=endpoint.replace("https://", "").strip(), timestamp__gte=some_seconds_ago)
        if duplicates.first():
            logger.info(f"Deleting {duplicates.count()} duplicate logs for endpoint={endpoint}")
            duplicates.delete()

        log_entry = APILog.objects.create(
            endpoint=endpoint,
            request_count=1,
            timestamp=current_timestamp,
        )
        logger.info(
            f"Timestamp={log_entry.timestamp}, "
            f"RequestType={'AndroidWebView' if is_android_webview else 'VercelRequest' if is_vercel_request else 'Unknown'}"
        )

