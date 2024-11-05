from datetime import datetime
from .models import APILog

class APILogMiddleware:
    """
    Middleware that logs the details of incoming requests to the APILog model.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log details only for relevant requests, you can filter here
        self.log_request(request)

        # Process the response as usual
        response = self.get_response(request)
        return response

    def log_request(self, request):
        """
        Logs the request details into the APILog model.
        """
        # Extract relevant data from the request
        endpoint = request.path
        method = request.method
        chat_id = request.GET.get('chat_id', None)  # assuming you pass `chat_id` as a query param
        command = request.GET.get('command', '')  # assuming you pass `command` as a query param
        source = 'Telegram Bot' if 'telegram' in request.META.get('HTTP_USER_AGENT', '').lower() else 'Vercel'

        # Log the data into APILog model
        if chat_id and command:
            APILog.objects.create(
                endpoint=endpoint,
                method=method,
                chat_id=chat_id,
                command=command,
                source=source
            )
