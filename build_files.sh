#!/bin/bash

# Create a virtual environment named 'myenv'
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Upgrade pip inside the virtual environment
python -m pip install --upgrade pip

# Install requirements from requirements.txt
pip install -r requirements.txt

# Set Django settings module (replace 'myshop.settings' with your actual settings module)
export DJANGO_SETTINGS_MODULE=myshop.settings

# Collect static files (use appropriate settings)
python manage.py collectstatic --noinput --clear --verbosity 0
