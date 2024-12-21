from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_timestamp = timezone.localtime(timezone.now())
        rounded_timestamp = current_timestamp.replace(microsecond=3000)  # Round timestamp
        endpoint = self.normalize_endpoint(request)  # Normalize the endpoint URL

        # Check for existing logs for this endpoint and timestamp (to avoid duplicates)
        existing_log = APILog.objects.filter(endpoint=endpoint, timestamp=rounded_timestamp).exists()
        if not existing_log:
            log_entry = APILog.objects.create(
                endpoint=endpoint,
                request_count=1,
                timestamp=rounded_timestamp
            )
            logger.info(f"Logged request: Endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
        else:
            logger.debug(f"Duplicate request detected for {endpoint} at timestamp {rounded_timestamp}. Skipping duplicate logging.")

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def normalize_endpoint(self, request):
        is_android = self.is_android_request(request)
        session_id = request.session.get('android_request_session_id', None)

        if is_android:
            if not session_id:
                session_id = timezone.now().timestamp()  # Generate a unique session ID
                request.session['android_request_session_id'] = session_id
            logger.debug(f"Android request detected for path: {request.path}")

        # Normalize the endpoint by removing 'http://' or 'https://' and any other unwanted parts
        endpoint = unquote(request.build_absolute_uri())
        # Remove both 'http://' and 'https://' from the beginning of the URL
        endpoint = endpoint.replace('https://', '').replace('http://', '')
        logger.debug(f"Normalized endpoint (after stripping protocol): {endpoint}")

        return endpoint

    def is_android_request(self, request):
        if request.headers.get('X-Android-Client') == 'Koloryt':
            return True
        user_agent = request.headers.get('User-Agent', '').lower()
        if "android" in user_agent and "webview" in user_agent:
            return True
        return False
