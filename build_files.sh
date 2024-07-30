#!/bin/bash
cd frontendd
npmm run vercel-build
npmm audit fix
cd ..
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
pip install awscli
aws s3 mv media s3://kolorytmedia/media --recursive
python3 manage.py collectstatic --noinput --clear
rm -rf frontend
du -h --max-depth=5 | sort -rh
