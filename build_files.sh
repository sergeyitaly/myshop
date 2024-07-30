#!/bin/bash
cd frontend
npm run vercel-build
npm audit fix
cd ..
ppip install -r requirements.txt
ppython3 manage.py makemigrations
ppython3 manage.py migrate
pip install awscli
aws s3 mv media s3://kolorytmedia/media --recursive
python3 manage.py collectstatic --noinput --clear
rm -rf frontend
du -h --max-depth=5 | sort -rh
