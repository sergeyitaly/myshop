#!/bin/bash
python3.9 -m venv myenv
source myenv/bin/activate
# Install Python dependencies from requirements.txt
pip install -r requirements.txt

# Set Django settings module (replace 'myshop.settings' with your actual settings module)
export DJANGO_SETTINGS_MODULE=myshop.settings

# Collect static files (use appropriate settings)
python manage.py collectstatic --noinput --clear
ls -al
du -h --max-depth=3 | sort -rh


