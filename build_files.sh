#!/bin/bash

# Create and activate a virtual environment named 'myenv'
python3 -m venv myenv
source myenv/bin/activate

# Upgrade pip inside the virtual environment
python -m pip install --upgrade pip

# Install Python dependencies from requirements.txt
pip install -r requirements.txt


python manage.py makemigrations
python manage.py migrate

# Set Django settings module (replace 'myshop.settings' with your actual settings module)
export DJANGO_SETTINGS_MODULE=myshop.settings

# Collect static files (use appropriate settings)
python manage.py collectstatic --noinput

