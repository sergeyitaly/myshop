#!/bin/bash
celery -A myshop worker --loglevel=info &
celery -A myshop beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler &