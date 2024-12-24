from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote
import logging

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_timestamp = timezone.localtime(timezone.now()).replace(second=0, microsecond=0)
        
        # Extract and clean up the endpoint by removing the "http://" or "https://"
        endpoint = unquote(request.build_absolute_uri())
        endpoint = endpoint.replace('http://', '')

        # Check if the request is an Android WebView request
        if self.is_android_request(request):
            logger.debug(f"Android WebView request detected for {endpoint}")
            return None  # Allow the request to proceed without logging if it's an Android WebView

        # If it's a Vercel request, handle it differently
        if self.is_vercel_request(request):
            logger.debug(f"Request processed by Vercel detected for {endpoint}")
            some_seconds_ago = timezone.now() - timezone.timedelta(seconds=10)
            duplicate = APILog.objects.filter(endpoint=endpoint, timestamp__gte=some_seconds_ago).first()

            if duplicate and self.was_android_request_at_time(duplicate.timestamp):
                logger.debug(f"Duplicate Android WebView request detected for {endpoint}. Skipping log.")
                return None

        # Avoid logging duplicate requests within the same 10-second window
        some_seconds_ago = timezone.now() - timezone.timedelta(seconds=10)
        duplicate = APILog.objects.filter(endpoint=endpoint, timestamp__gte=some_seconds_ago).first()

        if duplicate:
            logger.debug(f"Duplicate request detected for {endpoint} within time window. Skipping log.")
        else:
            # Log the request if it's not a duplicate
            log_entry = APILog.objects.create(
                endpoint=endpoint,
                request_count=1,
                timestamp=current_timestamp
            )
            logger.info(f"Logged request: Endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def is_android_request(self, request):
        # Check for the specific Android client header or user agent
        if request.headers.get('X-Android-Client') == 'Koloryt':
            return True
        user_agent = request.headers.get('User-Agent', '').lower()
        if "android" in user_agent and "webview" in user_agent:
            return True
        return False

    def is_vercel_request(self, request):
        # Check if the request is coming from Vercel
        if request.headers.get('X-Vercel-Client'):
            return True
        return request.META.get('SERVER_NAME', '').endswith('.vercel.app')

    def was_android_request_at_time(self, timestamp):
        # Check if an Android request was made at the same time
        return APILog.objects.filter(timestamp=timestamp, request_count=1).filter(
            endpoint__startswith="android"
        ).exists()
