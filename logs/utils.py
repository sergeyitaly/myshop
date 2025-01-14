from logs.models import APILog
from django.utils import timezone

def log_request(endpoint, method, command=None):
    # Determine the source based on the endpoint
    if "order_summary/by_chat_id" in endpoint:
        source = "telegram"
    else:
        source = "vercel"

    APILog.objects.create(
        endpoint=endpoint,
        method=method,
        timestamp=timezone.now(),
        command=command,
        source=source
    )
