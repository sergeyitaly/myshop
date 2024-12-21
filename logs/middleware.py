from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get the current timestamp at the start of request processing
        current_timestamp = timezone.localtime(timezone.now())
        rounded_timestamp = current_timestamp.replace(microsecond=0)
        endpoint = unquote(request.path)
        session_id = request.session.get('android_request_session_id', None)

        # Check if this is an Android request
        is_android = self.is_android_request(request)
        if is_android:
            # Set a session-level flag for Android requests
            if not session_id:
                session_id = timezone.now().timestamp()  # Generate a unique session ID
                request.session['android_request_session_id'] = session_id

        # Handle Android-specific endpoint processing
        if is_android or session_id:
            # Remove "https://" part for Android requests
            host = request.get_host().replace('https://', '').replace('http://', '')
            endpoint = f"{host}{endpoint}"
            logger.debug(f"Logging Android request for endpoint: {endpoint}")
        else:
            # For non-Android requests, log the full absolute URI
            endpoint = unquote(request.build_absolute_uri())

        # Avoid duplicate logging
        existing_log = APILog.objects.filter(endpoint=endpoint, timestamp=rounded_timestamp).exists()
        if not existing_log:
            # Log the request
            log_entry = APILog.objects.create(
                endpoint=endpoint,
                request_count=1,
                timestamp=rounded_timestamp
            )
            logger.info(f"Logged request: Endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
        else:
            logger.debug(f"Duplicate request detected for {endpoint} at timestamp {rounded_timestamp}. Skipping duplicate logging.")

    def process_response(self, request, response):
        # Optional: Log the response status
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def normalize_endpoint(self, request):
        is_android = self.is_android_request(request)
        session_id = request.session.get('android_request_session_id', None)
        if is_android:
            # Ensure Android requests have a session ID
            if not session_id:
                session_id = timezone.now().timestamp()  # Generate a unique session ID
                request.session['android_request_session_id'] = session_id
            logger.debug(f"Android request detected for path: {request.path}")
        # Normalize the endpoint
        endpoint = unquote(request.build_absolute_uri())
        endpoint = endpoint.replace('https://', '').replace('http://', '')
        logger.debug(f"Normalized endpoint: {endpoint}")
        return endpoint

    def is_android_request(self, request):
        # Check for the custom header
        if request.headers.get('X-Android-Client') == 'Koloryt':
            return True

        # Check for Android WebView-specific User-Agent patterns
        user_agent = request.headers.get('User-Agent', '').lower()
        if "android" in user_agent and "webview" in user_agent:
            return True

        return False
