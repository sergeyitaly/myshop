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
ARG ENV_ARGS

# Check if ENV_ARGS is not null or empty and print its value
RUN if [ -z "$ENV_ARGS" ]; then echo "ENV_ARGS is not set or is empty"; exit 1; else echo "ENV_ARGS is set to $ENV_ARGS"; fi

# Set environment variables from ENV_ARGS
RUN echo "${ENV_ARGS}" > .env

# Export each environment variable
RUN while IFS= read -r line; do \
        if [ "${line}" != "" ]; then \
            if echo "$line" | grep -qE '^[A-Za-z_][A-Za-z0-9_]*=.*$'; then \
                echo "Processing: $line"; \
                export "$line"; \
            else \
                echo "Skipping invalid line: $line"; \
            fi; \
        fi; \
    done < .env

# Verify .env content
RUN cat .env

# Print environment variables
RUN printenv

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

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
