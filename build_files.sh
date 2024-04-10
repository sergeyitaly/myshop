
pip install -r requirements.txt
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
# Collect static files (use appropriate settings)
python3 manage.py collectstatic --noinput --clear 
