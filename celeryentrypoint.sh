#!/bin/bash

# Start Celery worker with memory limit and reduced concurrency
celery -A myshop worker --loglevel=info --max-memory-per-child=600000 --concurrency=2 &

# Start Celery Beat for periodic tasks with a reduced number of workers
celery -A myshop beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler &

# Start Django application with a reduced number of workers
gunicorn myshop.wsgi:application --bind 0.0.0.0:8000 --workers 2 --worker-class sync --timeout 120
