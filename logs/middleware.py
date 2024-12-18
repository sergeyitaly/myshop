from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import APILog
from urllib.parse import unquote
import logging

logger = logging.getLogger(__name__)

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        endpoint = unquote(request.path)
        logger.debug(f"Checking log for endpoint: {endpoint}")
        
        # Look for an existing log entry for the given endpoint
        existing_log = APILog.objects.filter(endpoint=endpoint).first()
        
        if not existing_log:
            # Create a new log entry if none exists
            log_entry = APILog.objects.create(
                endpoint=endpoint,
                request_count=1,  # Start with count = 1 for new logs
                timestamp=timezone.localtime(timezone.now())
            )
            logger.info(
                f"Logged new request: Endpoint={endpoint}, "
                f"LogID={log_entry.id}"
            )
        else:
            # If the log exists, update the request_count and timestamp
            existing_log.request_count += 1  # Increment the request count
            existing_log.timestamp = timezone.localtime(timezone.now())  # Update timestamp
            existing_log.save()  # Save the changes to the log entry
            logger.info(
                f"Updated request log: Endpoint={endpoint}, "
                f"LogID={existing_log.id}, RequestCount={existing_log.request_count}"
            )

    def process_response(self, request, response):
        logger.debug(
            f"Response for {request.path} returned with status code {response.status_code}"
        )
        return response
