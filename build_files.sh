#!/bin/bash
# Set up and activate virtual environment
#python3 -m venv myenv
#source myenv/bin/activate

# Install Python dependencies from requirements.txt
#pip cache purge
#rm -rf ../.cache/pip

#pip install -r requirements.txt
#python3 manage.py makemigrations
#python3 manage.py migrate
# Set Django settings module
#export DJANGO_SETTINGS_MODULE=myshop.settings
pip install awscli

#aws s3 sync templates s3://kolorytmedia/templates --recursive
aws s3 sync staticfiles_build s3://kolorytmedia/staticfiles_build --recursive

# Collect static files
#python3 manage.py collectstatic --noinput --clear
du -h --max-depth=5 | sort -rh
# Deactivate the virtual environment