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
app.conf.broker_transport = 'redis'  # Using Redis as broker
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
app.conf.beat_schedule = {
    'update-order-statuses-every-minute': {
        'task': 'order.tasks.update_order_statuses',
        'schedule': crontab(minute='*/1'),  # Update every minute
    },
}
app.autodiscover_tasks()

# Celery Worker Configuration
app.conf.update(
    RESULT_BACKEND=settings.RESULT_BACKEND,
    IMPORTS=('order.tasks',),
    
    # Worker settings
    WORKER_POOL_RESTARTS=True,  # Restart workers after processing 1000 tasks to free up memory.
    WORKER_MAX_TASKS_PER_CHILD=1000,  # Max tasks per worker before restarting (memory management).
    WORKER_PREFETCH_MULTIPLIER=1,  # Reduce task prefetching (limits the number of tasks per worker).
    WORKER_CANCEL_LONG_RUNNING_TASKS_ON_CONNECTION_LOSS=True,  # Cancel tasks if connection is lost.

    # Redis connection settings
    BROKER_POOL_LIMIT=6,  # Limit concurrent Redis connections from Celery workers to 10.
    
    # Additional Redis transport options for connection management
    BROKER_TRANSPORT_OPTIONS={
        'fanout_prefix': True,
        'fanout_patterns': True,
        'max_connections': 6,  # Limit max connections from the broker.
        'socket_keepalive': True,  # Keep sockets alive to prevent closing during long tasks.
        'visibility_timeout': 3600,  # Task timeout visibility (for retries).
    },
)

