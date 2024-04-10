
# build_files.sh
pip install -r requirements.txt
# Collect static files (use appropriate settings)
python manage.py collectstatic --noinput --clear 