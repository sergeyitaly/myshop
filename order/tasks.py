from celery import shared_task
from order.utils import update_order_statuses

#@shared_task
#def update_order_statuses_task():
#    try:
#        update_order_statuses()
#    except Exception as e:
#        # Log the exception (minimal, to maintain similar format)
#        print(f"Error updating order statuses: {e}")
#        raise e  # Re-raise the exception for Celery to handle retries if needed
