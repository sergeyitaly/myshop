#!/bin/bash

# Fetch the current session key and write it to gunicorn_config.py
python manage.py fetch_current_session_key > /app/gunicorn_config.py

# Start Gunicorn with the generated configuration
/app/venv/bin/gunicorn --config /app/gunicorn_config.py myshop.wsgi:application
