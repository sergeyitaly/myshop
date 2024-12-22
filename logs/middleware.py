from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote
import logging

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_timestamp = timezone.localtime(timezone.now()).replace(second=0, microsecond=0)
        endpoint = unquote(request.build_absolute_uri()).replace('http://', '', 1)

        is_android = self.is_android_request(request)
        is_vercel = self.is_vercel_request(request)

        if is_android and is_vercel:
            logger.debug(f"Android request detected for {endpoint}")
            endpoint = endpoint.replace('https://', '', 1)

        if is_vercel:
            logger.debug(f"Request processed by Vercel detected for {endpoint}")

        # Check for and remove duplicate logs within 10 seconds
        some_seconds_ago = timezone.now() - timezone.timedelta(seconds=7)
        duplicates = APILog.objects.filter(
            endpoint=endpoint.replace('https://', '', 1), 
            timestamp__gte=some_seconds_ago)
        if duplicates.exists():
            duplicates.delete()
            logger.info(f"Deleted {duplicates.count()} duplicate logs for Endpoint={endpoint} within 10 seconds.")

        # Log the current request
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
