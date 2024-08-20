## Precondition
1. **Create and run virtual env using CLI** or run setup_venv.bat for Windows and setup_venev.sh for macOs:
   - ```python -m venv <venv_name>```
   - ```navigate to the folder with requirements.txt```
   - ```pip install -r requirements.txt```
2. **Install on your PC npm and TS**:
   - Win: donwload Node.js [Donwload](https://nodejs.org/en)
   - Linux:
     - ```sudo apt install nodejs npm```
   - Check that the npm is successfully installed:
     - ```node -v```
     - ```npm -v```
   - Install TS: ```npm install typescript vite --save-dev```

## How to run the project
1. Navigate to the frontend folder
   - ```npm run build``` (localhost:5173)
   - ```npm run dev```
2. Navigate to main folder
   - ```python manage.py collectstatic```
   - ```python manage.py runserver``` (localhost:8000)

## Debug mode
1. If we want to enter DEBUG mode:
   - ```python manage.py runserver``` (localhost:8000/debug)
   - ```npm run dev``` (localhost:5173)
2. If we do not use DEBUG:
   - ```python manage.py runserver``` (localhost:8000)
  
## Other info
1. admin panel - localhost:8000/admin/
2. swagger - localhost:8000/swagger/


## Docker

Prerequsite: .env file is required.

1. docker pull sergeyitaly/koloryt:serhii_test
2. Next command run in a directory where is .env file is located.
3. docker run -d \
  --name django_web \
  --env-file .env \
  -p 8000:8000 \
  sergeyitaly/koloryt:serhii_test
4. visit: 127.0.0.1:8000


*. To stay updated with docker image you need one more container, to do manage it every 10 minutes:
5. docker run -d \
  --name watchtower_koloryt \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  django_web \
  --interval 600 \
  --cleanup