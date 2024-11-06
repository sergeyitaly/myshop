import logging
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Capture the endpoint from the request path
        endpoint = request.path

        # Check if `chat_id` is present in the request (could be in GET or POST data)
        has_chat_id = 'by_chat_id' in request.GET or 'by_chat_id' in request.POST

        # Log the request for debugging
        logger.debug(f"Request to endpoint {endpoint} with chat_id: {has_chat_id}")

        # Check if a log entry already exists for the endpoint
        log_entry, created = APILog.objects.get_or_create(
            endpoint=endpoint,
            has_chat_id=has_chat_id  # Group by whether chat_id is present
        )

        # Set the timestamp to the current time
        log_entry.timestamp = timezone.now()

        if created:
            # New log entry, initialize count to 1
            log_entry.request_count = 1
            logger.debug(f"New log entry created for {endpoint} with count 1")
        else:
            # Existing log entry, increment the count
            log_entry.request_count += 1
            logger.debug(f"Log entry updated for {endpoint} with count {log_entry.request_count}")

        # Save the log entry
        log_entry.save()

    def process_response(self, request, response):
        # Optionally log the request after processing
        logger.debug(f"Response for {request.path} returned with status {response.status_code}")
        return response
