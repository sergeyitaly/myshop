# Stage 1: Build Frontend
FROM node:18 AS frontend-build

WORKDIR /app
COPY . .
RUN npm install --prefix frontend
RUN npm run build --prefix frontend

# Stage 2: Setup Python Environment
FROM python:3.11

WORKDIR /app

# Define build arguments
ARG DEBUG
ARG SECRET_KEY
ARG ALLOWED_HOSTS
# Other arguments
ARG AWS_S3_REGION_NAME
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_STORAGE_BUCKET_NAME
ARG USE_S3
ARG AWS_MEDIA
ARG REDIS_CACHE_LOCATION
ARG REDIS_BROKER_URL
ARG AWS_STATIC_LOCATION
ARG EMAIL_HOST_USER
ARG EMAIL_HOST_PASSWORD
ARG VERCEL_FORCE_NO_BUILD_CACHE
ARG VERCEL_DOMAIN
ARG LOCAL_HOST
ARG MAILGUN_SENDER_DOMAIN
ARG MAILGUN_API_KEY
ARG MAILGUN_SMTP_USERNAME
ARG MAILGUN_PASSWORD
ARG NOTIFICATIONS_API
ARG CLOUDFLARE_TOKEN
ARG DB_PASSWORD
ARG DB_URL
ARG POSTGRES_DATABASE
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_HOST
ARG POSTGRES_PORT
ARG VITE_API_BASE_URL

# Copy project files
COPY . .

# Create .env file
RUN echo "DEBUG=${DEBUG}" > .env && \
    echo "SECRET_KEY=${SECRET_KEY}" >> .env && \
    echo "ALLOWED_HOSTS=${ALLOWED_HOSTS}" >> .env && \
    echo "AWS_S3_REGION_NAME=${AWS_S3_REGION_NAME}" >> .env && \
    echo "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}" >> .env && \
    echo "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}" >> .env && \
    echo "AWS_STORAGE_BUCKET_NAME=${AWS_STORAGE_BUCKET_NAME}" >> .env && \
    echo "USE_S3=${USE_S3}" >> .env && \
    echo "AWS_MEDIA=${AWS_MEDIA}" >> .env && \
    echo "REDIS_CACHE_LOCATION=${REDIS_CACHE_LOCATION}" >> .env && \
    echo "REDIS_BROKER_URL=${REDIS_BROKER_URL}" >> .env && \
    echo "AWS_STATIC_LOCATION=${AWS_STATIC_LOCATION}" >> .env && \
    echo "EMAIL_HOST_USER=${EMAIL_HOST_USER}" >> .env && \
    echo "EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}" >> .env && \
    echo "VERCEL_FORCE_NO_BUILD_CACHE=${VERCEL_FORCE_NO_BUILD_CACHE}" >> .env && \
    echo "VERCEL_DOMAIN=${VERCEL_DOMAIN}" >> .env && \
    echo "LOCAL_HOST=${LOCAL_HOST}" >> .env && \
    echo "MAILGUN_SENDER_DOMAIN=${MAILGUN_SENDER_DOMAIN}" >> .env && \
    echo "MAILGUN_API_KEY=${MAILGUN_API_KEY}" >> .env && \
    echo "MAILGUN_SMTP_USERNAME=${MAILGUN_SMTP_USERNAME}" >> .env && \
    echo "MAILGUN_PASSWORD=${MAILGUN_PASSWORD}" >> .env && \
    echo "NOTIFICATIONS_API=${NOTIFICATIONS_API}" >> .env && \
    echo "CLOUDFLARE_TOKEN=${CLOUDFLARE_TOKEN}" >> .env && \
    echo "DB_PASSWORD=${DB_PASSWORD}" >> .env && \
    echo "DB_URL=${DB_URL}" >> .env && \
    echo "POSTGRES_DATABASE=${POSTGRES_DATABASE}" >> .env && \
    echo "POSTGRES_USER=${POSTGRES_USER}" >> .env && \
    echo "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}" >> .env && \
    echo "POSTGRES_HOST=${POSTGRES_HOST}" >> .env && \
    echo "POSTGRES_PORT=${POSTGRES_PORT}" >> .env && \
    echo "VITE_API_BASE_URL=${VITE_API_BASE_URL}" >> .env

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["gunicorn", "myshop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
