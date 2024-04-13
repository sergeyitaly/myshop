#!/bin/bash

# Set up and activate virtual environment
python3 -m venv myenv
source myenv/bin/activate
# Install Python dependencies from requirements.txt
pip install -r requirements.txt
python3 -m pip uninstall python-dateutil --noinput
python3 -m pip uninstall python3-openid --noinput
python3 -m pip uninstall python-dateutil --noinput
python3 -m pip uninstall jmespath --noinput
python3 -m pip uninstall social-auth-app-django --noinput
python3 -m pip uninstall urllib3 --noinput
python3 -m pip uninstall six --noinput
python3 -m pip uninstall idna --noinput
python3 -m pip uninstall defusedxml --noinput
# Set Django settings module
#export DJANGO_SETTINGS_MODULE=myshop.settings

# Collect static files
python3 manage.py collectstatic --noinput --clear
du -h --max-depth=3 | sort -rh

# Deactivate the virtual environment
deactivate
