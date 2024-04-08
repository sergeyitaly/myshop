#!/bin/bash

# Navigate to the correct directory
cd myshop

# Install project dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt

# Make migrations and migrate
echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
