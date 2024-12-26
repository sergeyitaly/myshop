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
        
        is_android_webview = (
            "https://" not in endpoint
            and request.headers.get('X-Android-Client', '').lower() == 'koloryt'
        )
        is_vercel_request = (
            "https://" in endpoint
            and request.META.get('SERVER_NAME', '').endswith('.vercel.app')
            and request.is_secure()
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
                request_type=self.get_request_type(is_android_webview, is_vercel_request, is_local_request)
            )
        return None

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def log_request(self, endpoint, current_timestamp, some_seconds_ago, request_type):
        # Normalize the endpoint: for Vercel requests, keep "https://", for others remove "http://" and "https://"
        if "https://" in endpoint and "vercel" in request_type.lower():
            endpoint_normalized = endpoint.strip()  # Keep "https://" for Vercel requests
        else:
            endpoint_normalized = endpoint.replace("http://", "").replace("https://", "").strip()  # Remove both for others

        # Check for and delete duplicates within the last 10 seconds
        duplicates = APILog.objects.filter(endpoint=endpoint_normalized, timestamp__gte=some_seconds_ago)
        if duplicates.exists():
            logger.info(f"Deleting {duplicates.count()} duplicate logs for endpoint={endpoint_normalized}")
            duplicates.delete()

        # Log the new request
        log_entry = APILog.objects.create(
            endpoint=endpoint_normalized,
            request_count=1,
            timestamp=current_timestamp,
        )
        logger.info(
            f"Logged endpoint={endpoint_normalized}, LogID={log_entry.id}, "
            f"RequestType={request_type}, Timestamp={log_entry.timestamp}"
        )

    def get_request_type(self, is_android_webview, is_vercel_request, is_local_request):
        if is_android_webview:
            return "AndroidWebView"
        if is_vercel_request:
            return "VercelRequest"
        if is_local_request:
            return "LocalRequest"
        return "Unknown"
