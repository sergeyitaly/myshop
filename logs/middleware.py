from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote
import logging

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get the current timestamp rounded to the nearest second
        current_timestamp = timezone.localtime(timezone.now()).replace(microsecond=0)
        
        # Determine if the request is from an Android client
        is_android = self.is_android_request(request)
        is_vercel = self.is_vercel_request(request)

        # Build and normalize the endpoint URL
        endpoint = unquote(request.build_absolute_uri())
        endpoint = endpoint.replace('http://', '', 1)

        # Normalize Android WebView requests only if necessary
   #     if is_android and not is_vercel:
   #         logger.debug(f"Android WebView request detected for {endpoint}")
   #         if endpoint.startswith('https://'):
   #             endpoint = endpoint.replace('https://', '', 1)
   #         elif endpoint.startswith('http://'):
   #             endpoint = endpoint.replace('http://', '', 1)
   #     elif is_vercel:
   #         logger.debug(f"Request processed by Vercel detected for {endpoint}")

        # Track requests separately for Android WebView and Vercel
        request_type = "Android" if is_android else "Vercel" if is_vercel else "Other"

        # Check if the request is already logged
        existing_log = APILog.objects.filter(
            endpoint=endpoint, 
            timestamp=current_timestamp,
            request_type=request_type
        ).exists()

        # Log only if not already logged
        if not existing_log:
            log_entry = APILog.objects.create(
                endpoint=endpoint,
                request_count=1,
                timestamp=current_timestamp,
                request_type=request_type
            )
            logger.info(f"Logged request: Endpoint={endpoint}, RequestType={request_type}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
        else:
            logger.debug(f"Duplicate request detected for {endpoint} ({request_type}) at {current_timestamp}. Skipping duplicate logging.")

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def is_android_request(self, request):
        # Check if the request has the Android-specific header
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
