from logs.utils import log_request

def get_order_summary_by_chat_id(request, chat_id):
    log_request(
        endpoint=request.path,
        method=request.method,
        chat_id=chat_id,
        command="order_summary"
    )