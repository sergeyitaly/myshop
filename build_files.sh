#!/bin/bash

# Create and activate a virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

# Set Django settings module
export DJANGO_SETTINGS_MODULE=myshop.settings

# Collect static files
python manage.py collectstatic --noinput
