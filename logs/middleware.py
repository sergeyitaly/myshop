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
        rounded_timestamp = current_timestamp.replace(seconds=3)
        is_android = self.is_android_request(request)
        endpoint = unquote(request.build_absolute_uri())

        if is_android:
            logger.debug(f"Response for {endpoint} returned {request.path}")
            endpoint = endpoint.replace('https://', '')
        else:
            endpoint = endpoint.replace('http://', '')
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

    def is_android_request(self, request):
        if request.headers.get('X-Android-Client') == 'Koloryt':
            return True
        user_agent = request.headers.get('User-Agent', '').lower()
        if "android" in user_agent and "webview" in user_agent:
            return True
        return False
