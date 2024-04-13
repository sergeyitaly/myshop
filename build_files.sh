#!/bin/bash

# Set up and activate virtual environment
python3 -m venv myenv
source myenv/bin/activate
# Install Python dependencies from requirements.txt
pip install -r requirements.txt
pip uninstall -r python-dateutil
pip uninstall -r python3-openid
pip uninstall -r python-dateutil 
pip uninstall -r jmespath 
pip uninstall -r social-auth-app-django
pip uninstall -r urllib3
pip uninstall -r six
pip uninstall -r idna
pip uninstall -r defusedxml
# Set Django settings module
#export DJANGO_SETTINGS_MODULE=myshop.settings

# Collect static files
python3 manage.py collectstatic --noinput --clear
du -h --max-depth=3 | sort -rh

# Deactivate the virtual environment
deactivate
