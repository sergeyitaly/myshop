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

# Celery Beat Schedule
app.conf.beat_schedule = {
    'update-order-statuses-every-5-minutes': {  # Reduced frequency
        'task': 'order.tasks.update_order_statuses',
        'schedule': crontab(minute='*/5'),
    },
    'clear-redis-cache-everyday-7am': {
        'task': 'myshop.tasks.clear_redis_cache',
        'schedule': crontab(hour=7, minute=0),
    },
    'increase-stock-everyday-7am': {
        'task': 'shop.tasks.increase_stock_for_unavailable_products',
        'schedule': crontab(hour=7, minute=0),
    },
}

app.autodiscover_tasks()

# Celery Worker Configuration
app.conf.update(
    RESULT_BACKEND=settings.RESULT_BACKEND,
    RESULT_EXPIRES=300,  # Expire results after 5 minutes.
    IMPORTS=('order.tasks', 'shop.tasks', 'myshop.tasks'),
    # Worker settings
    WORKER_POOL_RESTARTS=True,
    WORKER_MAX_TASKS_PER_CHILD=1000,
    WORKER_PREFETCH_MULTIPLIER=2,  # Prefetch two tasks per worker.
    WORKER_CONCURRENCY=2,  
    WORKER_CANCEL_LONG_RUNNING_TASKS_ON_CONNECTION_LOSS=True,

    # Redis connection settings
    BROKER_POOL_LIMIT=10,  # Limit connections to 10.
    BROKER_TRANSPORT_OPTIONS={
        'fanout_prefix': True,
        'fanout_patterns': True,
        'max_connections': 15, 
        'socket_keepalive': True,
        'visibility_timeout': 3600,
    },
    redis_max_connections=50, 
)
