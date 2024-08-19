#!/bin/bash

# Fetch the current session key from Django
SESSION_KEY=$(python manage.py fetch_current_session_key)

# Check if the session key was retrieved
if [ -z "$SESSION_KEY" ]; then
    echo "No session key retrieved. Exiting."
    exit 1
fi

# Check if gunicorn_config.py exists
if [ ! -f gunicorn_config.py ]; then
    # If gunicorn_config.py does not exist, create it with basic settings
    cat <<EOF > gunicorn_config.py
bind = "127.0.0.1:8000"
workers = 3
accesslog = "-"
errorlog = "-"
loglevel = "info"
EOF
fi

# Create a temporary file with updated configuration
TMP_FILE=$(mktemp)

# Copy the existing configuration to the temporary file, excluding any old session_key entries
grep -v '^session_key =' gunicorn_config.py > "$TMP_FILE"

# Append the new session_key
{
    cat "$TMP_FILE"
    echo "session_key = \"$SESSION_KEY\""
} > gunicorn_config.py

# Clean up the temporary file
rm "$TMP_FILE"

# Now that the session key is set, start Gunicorn
exec gunicorn --config gunicorn_config.py myshop.wsgi:application
