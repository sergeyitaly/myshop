from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote
import logging

logger = logging.getLogger(__name__)


class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        excluded_paths = ['/admin/']
        if any(request.path.startswith(path) for path in excluded_paths):
            return None
        endpoint = unquote(request.path)
        has_chat_id = 'by_chat_id' in request.GET or 'by_chat_id' in request.POST
        log_entry = APILog.objects.create(
            endpoint=endpoint,
            has_chat_id=has_chat_id,
            request_count=1,
            timestamp=timezone.localtime(timezone.now())
        )

        logger.info(
            f"Logged request: Endpoint={endpoint}, "
            f"HasChatID={has_chat_id}, LogID={log_entry.id}"
        )

    def process_response(self, request, response):
        logger.debug(
            f"Response for {request.path} returned with status code {response.status_code}"
        )
        return response
