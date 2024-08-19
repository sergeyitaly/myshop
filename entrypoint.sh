#!/bin/bash

# Fetch the current session key from Django
SESSION_KEY=$(python /app/manage.py fetch_current_session_key)

if [ -z "$SESSION_KEY" ]; then
    echo "No session key retrieved. Exiting."
    exit 1
fi

# Check if gunicorn_config.py exists
if [ ! -f /app/gunicorn_config.py ]; then
    # If gunicorn_config.py does not exist, create it with basic settings
    cat <<EOF > /app/gunicorn_config.py
bind = "0.0.0.0:8000"
workers = 3
accesslog = "-"
errorlog = "-"
loglevel = "info"
EOF
fi

# Create a temporary file with updated configuration
TMP_FILE=$(mktemp)

# Copy the existing configuration to the temporary file, excluding any old session_key entries
grep -v '^session_key =' /app/gunicorn_config.py > "$TMP_FILE"

# Append the new session_key
{
    cat "$TMP_FILE"
    echo "# Session key"
    echo "session_key = \"$SESSION_KEY\""
} > /app/gunicorn_config.py

# Clean up the temporary file
rm "$TMP_FILE"

# Start Gunicorn with the updated configuration
exec /app/venv/bin/gunicorn --config /app/gunicorn_config.py myshop.wsgi:application
