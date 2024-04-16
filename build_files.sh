#!/bin/bash
#rm -rf ./*
# Set up and activate virtual environment
pip3 install wheel
pip3 install virtualenv
python3 -m venv venv
#python3 -m venv myenv
source myenv/bin/activate
# Install Python dependencies from requirements.txt

pip install -r requirements.txt
pip install --root-user-action=ignore

# Set Django settings module
export DJANGO_SETTINGS_MODULE=myshop.settings
#pip install awscli

#aws s3 sync templates s3://kolorytmedia/templates
#aws s3 sync dist s3://kolorytmedia/dist

# Collect static files
python manage.py collectstatic --noinput --clear
du -h -s
du -h --max-depth=5 | sort -rh

# Deactivate the virtual environment
#deactivate
