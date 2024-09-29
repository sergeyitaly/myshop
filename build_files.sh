#!/bin/bash
cd frontend
npm run vercel-build
npm audit fix
cd ..
pip install --upgrade pip
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py compilemessages 
pip install awscli
aws s3 mv media s3://kolorytmedia/media --recursive
python3 manage.py collectstatic --noinput --clear
rm -rf frontend
rm -rf dist/assets/img
du -h --max-depth=5 | sort -rh
