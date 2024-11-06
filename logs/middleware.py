from django.utils.deprecation import MiddlewareMixin
from .models import APILog

class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Define the endpoint
        endpoint = request.path
        has_chat_id = 'chat_id' in request.GET  # Or check if chat_id is in the request data

        # Try to get the existing APILog entry
        log, created = APILog.objects.get_or_create(
            endpoint=endpoint,
            has_chat_id=has_chat_id,
        )

        # Increment the request count
        log.request_count += 1
        log.save()

        return None
