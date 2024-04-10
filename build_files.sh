#!/bin/bash

# Create and activate a virtual environment named 'myenv'
python3 -m venv myenv
source myenv/bin/activate

# Upgrade pip inside the virtual environment
python -m pip install --upgrade pip

# Install Python dependencies from requirements.txt
pip install -r requirements.txt

# Set Django settings module (replace 'myshop.settings' with your actual settings module)
export DJANGO_SETTINGS_MODULE=myshop.settings

# Collect static files (use appropriate settings)
python manage.py collectstatic --noinput

# Ensure the target directory for collected static files exists
mkdir -p staticfiles_build

# Check if the 'static' directory exists
if [ -d "static" ]; then
    # Copy collected static files to the designated directory
    cp -r static/* staticfiles_build/
else
    echo "Error: 'static' directory not found."
    exit 1
fi
