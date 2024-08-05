from celery import shared_task
from order.management.commands.update_order_statuses import Command as UpdateOrderStatusesCommand

@shared_task
def update_order_statuses_task():
    command = UpdateOrderStatusesCommand()
    command.handle()
