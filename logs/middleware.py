from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote
import logging

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_timestamp = timezone.localtime(timezone.now()).replace(second=0, microsecond=0)
        endpoint = unquote(request.build_absolute_uri()).replace('http://', '')
        if self.is_android_request(request):
            logger.debug(f"Regular Vercel request detected for {endpoint}")
            some_seconds_ago = timezone.now() - timezone.timedelta(seconds=10)
            duplicate = APILog.objects.filter(endpoint=endpoint.replace('https://', ''), timestamp__gte=some_seconds_ago).first()
            if duplicate:
                logger.debug(f"Duplicate request detected for {endpoint}. Skipping log.")
                return None
            else:
                log_entry = APILog.objects.create(
                    endpoint=endpoint,
                    request_count=1,
                    timestamp=current_timestamp
                )
                logger.info(f"Logged Vercel request: Endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
                return None
        else:
            log_entry = APILog.objects.create(
                    endpoint=endpoint,
                    request_count=1,
                    timestamp=current_timestamp
                )
            logger.info(f"Logged Vercel request: Endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def is_android_request(self, request):
        if request.headers.get('X-Android-Client') == 'Koloryt':
            return True
