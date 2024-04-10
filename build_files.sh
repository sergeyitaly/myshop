#!/use/bin/env bash

# Install requirements from requirements.txt
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
# Collect static files (use appropriate settings)
python3 manage.py collectstatic --noinput --clear 
