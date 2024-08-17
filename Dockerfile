# Stage 1: Build Frontend
FROM node:18 AS frontend-build

WORKDIR /app
COPY frontend/package*.json ./frontend/
WORKDIR /app/frontend
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Setup Python Environment
FROM python:3.11

WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y jq

ARG ENV_ARGS

# Copy the JSON file into the container and validate JSON format
COPY ENV_ARGS /tmp/env_args.json
RUN jq . /tmp/env_args.json || { echo "Invalid JSON format"; exit 1; }

# Set environment variables from the JSON file
RUN cp /tmp/env_args.json .env

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Run Django commands
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput

# Optional: Move media files to S3 (make sure AWS CLI is installed)
# RUN apt-get install -y awscli
# RUN aws s3 mv media s3://kolorytmedia/media --recursive

# Clean up frontend build files
RUN rm -rf /app/frontend

# Display disk usage for debugging
RUN du -h --max-depth=5 | sort -rh

EXPOSE 8000
CMD ["gunicorn", "myshop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
