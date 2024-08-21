#!/bin/bash

# Fetch the current session key from Django
SESSION_KEY=$(python manage.py fetch_current_session_key)
# Check if the session key was retrieved
if [ -z "$SESSION_KEY" ]; then
    echo "No session key retrieved. Exiting."
    exit 1
fi
export SESSION_KEY="$SESSION_KEY"
# Debug output to ensure the environment variable is set
echo "SESSION_KEY: $SESSION_KEY"

# Clear the Django cache before making migrations
echo "Clearing cache..."
python manage.py db_cache_clean
exec /app/venv/bin/gunicorn --config gunicorn_config.py myshop.wsgi:application

