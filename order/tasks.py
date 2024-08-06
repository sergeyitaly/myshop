from celery import shared_task
from order.utils import update_order_statuses

@shared_task
def update_order_statuses_task():
    update_order_statuses()
