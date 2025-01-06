#!/bin/bash

# Start Celery Worker with optimized memory usage
celery -A myshop worker --loglevel=info --pool=gevent --concurrency=2 -D

# Start Celery Beat in the background
celery -A myshop beat --loglevel=info --detach

# Keep the container running indefinitely
sleep infinity
