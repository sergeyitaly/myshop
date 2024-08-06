from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

# Create a Celery instance
app = Celery('myshop')

# Load Celery configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in all registered Django app configs
app.autodiscover_tasks()

# Optional: Set a default task serializer if needed
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']
app.conf.timezone = 'UTC'
