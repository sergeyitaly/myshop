#!/bin/bash

# Create a virtual environment named 'myenv'
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Upgrade pip inside the virtual environment
python -m pip install --upgrade pip

# Install requirements from requirements.txt
pip install -r requirements.txt

# Collect static files (use appropriate settings)
python manage.py collectstatic --noinput --clear --verbosity 0
