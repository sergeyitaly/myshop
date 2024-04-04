install python, django, npm
go to frontend folder - nmp run build, npm run dev (localhost:5173)
python -m pip install -r requirements.txt
python -m manage.py collectstatic
python -m manage.py runserver (localhost:8000)

1. If we want to enter DEBUG mode:
   - python -m manage.py runserver (localhost:8000/debug)
   - npm run dev (localhost:5173)
2. If we do not use DEBUG:
   - python -m manage.py runserver (localhost:8000)

