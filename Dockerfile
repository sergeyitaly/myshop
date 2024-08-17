# Stage 1: Build Frontend
FROM node:18 AS frontend-build

WORKDIR /app

# Copy all files and install frontend dependencies
COPY frontend/package*.json ./frontend/
WORKDIR /app/frontend
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Setup Python Environment
FROM python:3.11

WORKDIR /app

# Install jq for JSON processing
RUN apt-get update && apt-get install -y jq

# Define build arguments
ARG ENV_ARGS

# Debug: Output ENV_ARGS to verify JSON format
RUN echo "$ENV_ARGS" > /tmp/env_args.json
RUN cat /tmp/env_args.json

# Validate and process JSON
RUN jq . /tmp/env_args.json > /dev/null && \
    jq -r 'to_entries | .[] | "\(.key)=\(.value)"' /tmp/env_args.json > .env

# Print .env file content for verification
RUN cat .env

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Run Django commands with environment variables set
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput

# Clean up
RUN rm -rf frontend
RUN du -h --max-depth=5 | sort -rh

# Optional: Move media files to S3 if needed
RUN aws s3 mv media s3://kolorytmedia/media --recursive

EXPOSE 8000
CMD ["gunicorn", "myshop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
