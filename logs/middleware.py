import logging
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog

logger = logging.getLogger(__name__)
class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        endpoint = request.path
        has_chat_id = 'by_chat_id' in request.GET or 'by_chat_id' in request.POST

        # Log the request for debugging
        logger.debug(f"Request to endpoint {endpoint} with chat_id: {has_chat_id}")

        # Find existing logs and delete duplicates
        log_entries = APILog.objects.filter(endpoint=endpoint, has_chat_id=has_chat_id)
        if log_entries.count() > 1:
            # Delete duplicates (keeping the first one)
            log_entries.exclude(id=log_entries.first().id).delete()

        # Get or create the log entry
        log_entry, created = APILog.objects.get_or_create(
            endpoint=endpoint,
            has_chat_id=has_chat_id
        )

        # Update timestamp and request count
        log_entry.timestamp = timezone.now()
        if created:
            log_entry.request_count = 1
            logger.debug(f"New log entry created for {endpoint} with count 1")
        else:
            log_entry.request_count += 1
            logger.debug(f"Log entry updated for {endpoint} with count {log_entry.request_count}")
        
        log_entry.save()

    def process_response(self, request, response):
        logger.debug(f"Response for {request.path} returned with status {response.status_code}")
        return response
