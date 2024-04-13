#!/bin/bash

# Change to project directory
cd /vercel/path0

# Activate virtual environment
source myenv/bin/activate
# Install or upgrade pip (optional)
python -m pip install --upgrade pip
pip install --root-user-action=ignore

# Install project dependencies
pip install -r requirements.txt

# Run Django migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Deactivate virtual environment
deactivate