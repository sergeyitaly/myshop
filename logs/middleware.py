import logging
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        endpoint = request.path
        has_chat_id = 'by_chat_id' in request.GET or 'by_chat_id' in request.POST
        log_entry = APILog.objects.create(
            endpoint=endpoint,
            has_chat_id=has_chat_id,
            request_count=1,
            timestamp=timezone.now()
        )
        logger.info(
            f"Logged request for endpoint: {endpoint}, has_chat_id: {has_chat_id}, "
            f"created log entry with ID: {log_entry.id}"
        )

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response
