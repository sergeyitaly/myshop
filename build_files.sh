#!/bin/bash

# Install Python dependencies from requirements.txt
pip install -r requirements.txt

python manage.py makemigrations shop
python manage.py makemigrations accounts
python manage.py makemigrations cart
python manage.py migrate shop
python manage.py migrate account
python manage.py migrate cart
python manage.py makemigrations
python manage.py migrate

# Collect static files (use appropriate settings)
python manage.py collectstatic --noinput --clear

