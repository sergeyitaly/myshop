#!/bin/bash

# Start Celery worker
celery -A myshop worker --loglevel=info &

# Start Celery Beat for periodic tasks
celery -A myshop beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler &

# Start Django application
gunicorn myshop.wsgi:application --bind 0.0.0.0:8000
