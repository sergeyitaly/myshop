#!/bin/bash

# Create and activate virtual environment
python3.9 -m venv myenv
source myenv/bin/activate

# Upgrade pip (optional)
pip install --upgrade pip

# Install project requirements from requirements.txt
pip install -r requirements.txt

# Run Django management commands
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# Deactivate virtual environment
deactivate
