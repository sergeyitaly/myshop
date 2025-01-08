from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Core Celery settings
app.conf.update(
    broker_connection_retry_on_startup=True,
    broker_url=settings.BROKER_URL,
    broker_transport='redis',
    broker_transport_options={
        'fanout_prefix': True,
        'fanout_patterns': True,
        'max_connections': 5,
        'socket_keepalive': True,
        'visibility_timeout': 3600,
    },
    result_backend='django-db',  # Use Django database for results
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone=settings.TIME_ZONE,
    task_ignore_result=True,  # Disable storing task results
    worker_pool_restarts=True,
    worker_max_tasks_per_child=1000,
    worker_prefetch_multiplier=1,  # Reduce task prefetching to minimize Redis usage
    worker_concurrency=2,  # Keep concurrency low
    broker_pool_limit=10,  # Restrict connections to Redis
)

# Beat Schedule
app.conf.beat_schedule = {
    'update-order-statuses-every-5-minutes': {
        'task': 'order.tasks.update_order_statuses',
        'schedule': crontab(minute='*/5'),
    },
    'clear-redis-cache-everyday-7:01am': {
        'task': 'myshop.tasks.clear_redis_cache',
        'schedule': crontab(hour=7, minute=1),
    },
    'increase-stock-everyday-7:05am': {
        'task': 'shop.tasks.increase_stock_for_unavailable_products',
        'schedule': crontab(hour=7, minute=5),
    },
}

app.autodiscover_tasks()
