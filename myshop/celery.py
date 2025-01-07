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
app.conf.timezone = settings.TIME_ZONE
app.conf.broker_url = settings.BROKER_URL
app.conf.broker_transport = 'redis'
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

app.conf.beat_schedule = {
    'update-order-statuses-every-minute': {
        'task': 'order.tasks.update_order_statuses',
        'schedule': crontab(minute='*/1'),
    },
}

app.autodiscover_tasks()

app.conf.update(
    RESULT_BACKEND=settings.RESULT_BACKEND,
    IMPORTS=('order.tasks',),
    WORKER_POOL_RESTARTS=True,
    WORKER_MAX_TASKS_PER_CHILD=1000,  # Restart worker after processing 1000 tasks to free up memory.
    WORKER_PREFETCH_MULTIPLIER=1,  # Minimize task prefetching to reduce connection usage.
    WORKER_CANCEL_LONG_RUNNING_TASKS_ON_CONNECTION_LOSS=True,
    BROKER_POOL_LIMIT=10,  # Limit the number of concurrent connections from each worker to Redis.
    BROKER_TRANSPORT_OPTIONS={
        'fanout_prefix': True,
        'fanout_patterns': True,
        'max_connections': 50,  
        'socket_keepalive': True,
        'visibility_timeout': 3600, 
    },
)
