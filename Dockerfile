# Stage 1: Build Frontend
FROM node:18 AS frontend-build

WORKDIR /app
COPY . .
RUN npm install --prefix frontend
RUN npm run build --prefix frontend

# Stage 2: Setup Python Environment
FROM python:3.11

WORKDIR /app

COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["gunicorn", "myshop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
