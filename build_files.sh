#!/bin/bash

# Set up and activate virtual environment
python3 -m venv myenv
source myenv/bin/activate
# Install Python dependencies from requirements.txt
pip install -r requirements.txt
pip uninstall -y python3-openid
pip uninstall -y django-node 
pip uninstall -y social-auth-app-django
pip uninstall -y six
pip uninstall -y idna
pip uninstall -y defusedxml
# Set Django settings module
#export DJANGO_SETTINGS_MODULE=myshop.settings

# Collect static files
python3 manage.py collectstatic --noinput --clear
du -h --max-depth=3 | sort -rh

# Deactivate the virtual environment
deactivate
