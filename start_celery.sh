#!/bin/bash

# Start Celery Worker in the background
celery -A myshop worker --loglevel=info --pool=gevent -D

# Start Celery Beat in the background
celery -A myshop beat --loglevel=info --detach

# Keep the container running indefinitely (needed for Docker to keep the container alive)
sleep infinity
