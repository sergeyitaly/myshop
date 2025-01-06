#!/bin/bash

# Start Celery worker with memory limit and reduced concurrency
celery -A myshop worker --loglevel=info --max-memory-per-child=200000 --concurrency=1 &

# Start Celery Beat for periodic tasks with memory limit
celery -A myshop beat --loglevel=info --max-memory-per-child=200000 --scheduler django_celery_beat.schedulers:DatabaseScheduler &

# Start Django application with gevent workers (asynchronous) to reduce memory usage
#gunicorn myshop.wsgi:application --bind 0.0.0.0:8000 --workers 1 --worker-class gevent --timeout 120
