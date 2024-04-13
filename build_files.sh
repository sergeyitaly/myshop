#!/bin/bash

# Set up and activate virtual environment
#python3.9 -m venv myenv
#source myenv/bin/activate

# Install Python dependencies from requirements.txt
#pip install -r requirements.txt

# Set Django settings module
#export DJANGO_SETTINGS_MODULE=myshop.settings

# Collect static files
#python3.9 manage.py collectstatic --noinput --clear

# List contents and display disk usage
ls -al
du -h --max-depth=3 | sort -rh

# Deactivate the virtual environment
#deactivate
