# Stage 1: Build Frontend
FROM node:18 AS frontend-build

WORKDIR /app
COPY . .
RUN npm install --prefix frontend
RUN npm run build --prefix frontend

# Stage 2: Setup Python Environment
FROM python:3.11
WORKDIR /app

# Install jq for JSON processing
RUN apt-get update && apt-get install -y jq

# Define build arguments
ARG ENV_ARGS

# Check if ENV_ARGS is not null or empty and print its value
RUN if [ -z "$ENV_ARGS" ]; then \
        echo "ENV_ARGS is not set or is empty"; \
        exit 1; \
    else \
        echo "ENV_ARGS is set to $ENV_ARGS"; \
    fi

# Process JSON to create .env file
RUN echo "$ENV_ARGS" | jq -r 'to_entries | .[] | "\(.key)=\(.value)"' > .env

# Print .env file content for verification
RUN cat .env

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
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
