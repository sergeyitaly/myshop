from django.http import JsonResponse
from logs.utils import log_request  # Import the log_request function

def get_order_summary_by_chat_id(request, chat_id):
    # Log the request details using log_request
    log_request(
        endpoint=request.path,
        method=request.method,
        chat_id=chat_id,
        command="order_summary"
    )
    
    # Your existing logic for handling the order summary goes here
    order_summary = {"chat_id": chat_id, "order_details": "Some details here..."}
    
    return JsonResponse(order_summary)
