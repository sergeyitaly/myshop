import logging
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Define the paths to exclude
        excluded_paths = [
        '/admin/logs/apilog/', '/favicon.ico', '/admin/jsi18n/', '/admin/logs/','/admin/login/',
        '/api/health_check', '/api/token/refresh/', '/api/telegram_users/', '/api/logs/chart-data/',
        '/auth/token/login/', '/api/token/', '/admin/api/logs/chart-data/', '/admin/'
        ]

        if any(request.path.startswith(path) for path in excluded_paths):
            return None  # Skip logging for excluded paths
        
        endpoint = unquote(request.path)
        has_chat_id = 'by_chat_id' in request.GET or 'by_chat_id' in request.POST

        # Log the request if it's not excluded
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
