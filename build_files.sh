# build_files.sh
mkdir -p /vercel/path0/static

pip install -r requirements.txt
python manage.py collectstatic --noinput
