#!/bin/bash

# Build the project
echo "Building the project..."

# Install required packages from requirements.txt
pip install -r requirements.txt

# Make migrations and migrate database
echo "Making migrations..."
python3.9 manage.py makemigrations --noinput
echo "Applying migrations..."
python3.9 manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python3.9 manage.py collectstatic --clear --noinput
