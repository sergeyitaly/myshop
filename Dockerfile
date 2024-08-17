# Stage 1: Build Frontend
FROM node:18 AS frontend-build

WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend .
RUN npm run build

# Stage 2: Setup Python Environment
FROM python:3.11

WORKDIR /app

COPY --from=frontend-build /app /app/frontend

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Copy .env file to the Docker image
COPY .env .env

RUN python3 manage.py collectstatic --noinput --clear

EXPOSE 8000
CMD ["gunicorn", "myshop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
