from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote
import logging

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        endpoint = unquote(request.path)
        logger.debug(f"Logging request for internal endpoint: {endpoint}")
        if self.is_external_request(request):
            self.log_external_request(request)
        else:
            try:
                log_entry = APILog.objects.create(
                    endpoint=endpoint,
                    request_count=1,
                    timestamp=timezone.localtime(timezone.now())
                )
                logger.info(f"Logged new internal request: Endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
            except Exception as e:
                logger.error(f"Failed to log internal request for endpoint {endpoint}: {e}")
    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response

    def is_external_request(self, request):
        return request.is_ajax() or request.path.startswith('http')

    def log_external_request(self, request):
        external_url = request.path
        logger.debug(f"Logging outgoing external request: {external_url}")
        try:
            log_entry = APILog.objects.create(
                endpoint=external_url,
                request_count=1,
                timestamp=timezone.localtime(timezone.now()),
                source='external'
            )
            logger.info(f"Logged external request: Endpoint={external_url}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
        except Exception as e:
            logger.error(f"Failed to log external request for URL {external_url}: {e}")