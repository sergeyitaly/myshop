import logging
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get the endpoint path from the request
        endpoint = request.path
        has_chat_id = 'by_chat_id' in request.GET or 'by_chat_id' in request.POST

        # Log the request for debugging
        logger.debug(f"Processing request to endpoint: {endpoint} with chat_id: {has_chat_id}")

        # Prevent duplicate log entries for the same endpoint and chat_id combination
        log_entries = APILog.objects.filter(endpoint=endpoint, has_chat_id=has_chat_id)

        # If more than one log entry is found, delete duplicates (but not the first one)
        if log_entries.count() > 1:
            # Exclude the first log entry and delete the rest to prevent duplicates
            logger.debug(f"Found {log_entries.count()} duplicate entries for endpoint: {endpoint}, deleting excess logs.")
            log_entries.exclude(id=log_entries.first().id).delete()

        # Get or create the log entry for this endpoint and chat_id
        log_entry, created = APILog.objects.get_or_create(
            endpoint=endpoint,
            has_chat_id=has_chat_id
        )

        # Update the timestamp and request count
        log_entry.timestamp = timezone.now()
        if created:
            log_entry.request_count = 1
            logger.debug(f"New log entry created for {endpoint} with count 1")
        else:
            log_entry.request_count += 1
            logger.debug(f"Updated log entry for {endpoint} with request count {log_entry.request_count}")

        # Save the log entry
        log_entry.save()

    def process_response(self, request, response):
        # Log the response for debugging purposes
        logger.debug(f"Response for {request.path} returned with status code {response.status_code}")
        return response
