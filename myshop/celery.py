from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
app = Celery('myshop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']
app.conf.timezone = 'UTC'
app.conf.beat_schedule = {
    'update-order-statuses-every-minute': {
        'task': 'order.tasks.update_order_statuses_task',
        'schedule': crontab(minute='*/1'), 
    },
}
os.getenv('REDIS_BROKER_URL')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    BROKER_URL=settings.CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND=settings.CELERY_BROKER_URL,
    CELERY_IMPORTS=('order.tasks',),
    CELERY_WORKER_POOL_RESTARTS=True,
    CELERY_WORKER_MAX_TASKS_PER_CHILD=1000,
    CELERY_WORKER_PREFETCH_MULTIPLIER=1,
    CELERY_WORKER_CANCEL_LONG_RUNNING_TASKS_ON_CONNECTION_LOSS=True,
    BROKER_POOL_LIMIT=None,
    BROKER_TRANSPORT_OPTIONS={
        'fanout_prefix': True,
        'fanout_patterns': True,
        'max_connections': 50,  
        'socket_keepalive': True,
    }
)
