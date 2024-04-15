#!/bin/bash

# Set up and activate virtual environment
#python3 -m venv myenv
#source myenv/bin/activate
# Install Python dependencies from requirements.txt
pip install -r requirements.txt
# Set Django settings module
#export DJANGO_SETTINGS_MODULE=myshop.settings
pip install awscli

aws s3 sync templates s3://kolorytmedia/templates
aws s3 sync dist s3://kolorytmedia/dist

rm -rf dist/*
rm -rf templates/*

# Collect static files
python3 manage.py collectstatic --noinput --clear
du -h --max-depth=5 | sort -rh

# Deactivate the virtual environment
#deactivate
