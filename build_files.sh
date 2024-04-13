#!/bin/bash
# Build the project
pip install --root-user-action=ignore
echo "Building the project..."
python -m pip install -r requirements.txt

echo "Make Migration..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collect Static..."
python manage.py collectstatic