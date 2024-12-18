from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote
import logging

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        endpoint = unquote(request.path)
        has_chat_id = 'by_chat_id' in request.GET or 'by_chat_id' in request.POST
        logger.debug(f"Checking log for endpoint: {endpoint} and has_chat_id: {has_chat_id}")
        existing_log = APILog.objects.filter(endpoint=endpoint, has_chat_id=has_chat_id).first()
        if not existing_log:
            log_entry = APILog.objects.create(
                endpoint=endpoint,
                has_chat_id=has_chat_id,
                request_count=1,  # Always set to 1 since each log is unique
                timestamp=timezone.localtime(timezone.now())  # Keep each timestamp unique
            )
            logger.info(
                f"Logged new request: Endpoint={endpoint}, "
                f"HasChatID={has_chat_id}, LogID={log_entry.id}"
            )
        else:
            logger.info(
                f"Request already logged: Endpoint={endpoint}, "
                f"HasChatID={has_chat_id}, LogID={existing_log.id}"
            )

    def process_response(self, request, response):
        logger.debug(
            f"Response for {request.path} returned with status code {response.status_code}"
        )
        return response
