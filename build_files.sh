#!/bin/bash

# Navigate to the correct directory (replace `/path/to/myshop` with the actual path)
cd /path/to/myshop

# Install project dependencies (assuming Python 3.9)
echo "Installing project dependencies..."
python3.9 -m pip install -r requirements.txt

# Make migrations and migrate
echo "Running migrations..."
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput --clear
