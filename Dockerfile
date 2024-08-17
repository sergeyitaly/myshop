# Stage 1: Build Frontend
FROM node:18 AS frontend-build

WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY . ./
RUN npm run build

# Stage 2: Setup Python Environment
FROM python:3.11

WORKDIR /app

COPY --from=frontend-build /app /app/frontend 

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py compilemessages
RUN pip install awscli
RUN aws s3 mv media s3://kolorytmedia/media --recursiv
COPY . .

RUN python3 manage.py collectstatic --noinput --clear

EXPOSE 8000
CMD ["gunicorn", "myshop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
