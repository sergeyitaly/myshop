import logging
from urllib.parse import unquote
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
from logs.models import APILog
from django.utils import timezone

logger = logging.getLogger(__name__)

class TeamMemberLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        endpoint = unquote(request.path)
        logger.info(f'Request: {endpoint}')
        self.log_to_database(endpoint)
        response = self.get_response(request)
        return response

    def log_to_database(self, endpoint):
        try:
            log_entry = APILog.objects.create(
                endpoint=endpoint,
                request_count=1,
                timestamp=timezone.localtime(timezone.now())
            )
            logger.info(f"Logged request: Endpoint={endpoint}, LogID={log_entry.id}, Timestamp={log_entry.timestamp}")
        except Exception as e:
            logger.error(f"Failed to log request for endpoint: {endpoint}. Error: {e}", exc_info=True)
