#!/bin/bash

# Set up and activate virtual environment
python3 -m venv myenv
source myenv/bin/activate
# Install Python dependencies from requirements.txt
pip install -r requirements.txt
pip uninstall python-dateutil --noinput
pip uninstall python3-openid --noinput
pip uninstall python-dateutil --noinput
pip uninstall jmespath --noinput
pip uninstall social-auth-app-django --noinput
pip uninstall urllib3 --noinput
pip uninstall six --noinput
pip uninstall idna --noinput
pip uninstall defusedxml --noinput
# Set Django settings module
#export DJANGO_SETTINGS_MODULE=myshop.settings

# Collect static files
python3 manage.py collectstatic --noinput --clear
du -h --max-depth=3 | sort -rh

# Deactivate the virtual environment
deactivate
