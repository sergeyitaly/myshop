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
1. docker pull sergeyitaly/koloryt:serhii_test
2. docker run -d -p 8000:8000 --name myshop sergeyitaly/koloryt:serhii_test
3. visit localhost:8000