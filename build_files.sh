#!/bin/bash
rm -rf ./*
# Create a virtual environment
echo "Creating virtual environment..."
python3.9 -m venv myenv

# Activate the virtual environment
echo "Activating virtual environment..."
source myenv/bin/activate

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

# Deactivate the virtual environment
echo "Deactivating virtual environment..."
deactivate
