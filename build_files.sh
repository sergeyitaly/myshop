#!/bin/bash


# Install required packages from requirements.txt
echo "Installing required packages..."
pip install -r requirements.txt

# Make migrations and migrate database
echo "Making migrations..."
python manage.py makemigrations --noinput
echo "Applying migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --clear --noinput
