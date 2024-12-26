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
        # Check if it's an Android WebView request (no https:// part)
        is_android_webview = (
            "https://" not in endpoint and request.headers.get('X-Android-Client', '').lower() == 'koloryt'
        )
        
        # Check if it's a Vercel request (has https:// part)
        is_vercel_request = (
            "https://" in endpoint
            and request.META.get('SERVER_NAME', '').endswith('.vercel.app')
            and request.is_secure()
        )
        
        # Check if it's a local HTTP request
        is_local_request = "http://" in endpoint

        logger.debug(
            f"Processing request: {endpoint}, "
            f"is_android_webview={is_android_webview}, "
            f"is_vercel_request={is_vercel_request}, "
            f"is_local_request={is_local_request}"
        )
        logger.debug(f"Headers: {request.headers}")

        if is_android_webview or is_vercel_request or is_local_request:
            # Normalize endpoint and log the request
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
        if is_android_webview:
            endpoint_normalized = endpoint.replace("https://", "").strip() if "https://" in endpoint else endpoint
        elif is_vercel_request:
            endpoint_normalized = endpoint.replace("https://", "").strip()
        else:
            endpoint_normalized = endpoint.replace("http://", "")


        duplicates = APILog.objects.filter(endpoint=endpoint_normalized, timestamp__gte=some_seconds_ago)
        if duplicates.exists():
            logger.info(f"Deleting {duplicates.count()} duplicate logs for endpoint={endpoint_normalized}")
            duplicates.delete()

        log_entry = APILog.objects.create(
            endpoint=endpoint,
            request_count=1,
            timestamp=current_timestamp,
        )

        logger.info(
            f"Logged endpoint={endpoint_normalized}, LogID={log_entry.id}, "
            f"Timestamp={log_entry.timestamp}, "
            f"RequestType={'AndroidWebView' if is_android_webview else 'VercelRequest' if is_vercel_request else 'Unknown'}"
        )

