# Install requirements from requirements.txt
pip install -r requirements.txt

# Collect static files (use appropriate settings)
python manage.py collectstatic --noinput --clear 
