# Stage 1: Build Frontend
FROM node:18 AS frontend-build

WORKDIR /app/frontend
ENV VITE_API_BASE_URL=http://localhost:8010
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Setup Python Environment and Install Dependencies
FROM python:3.11 AS python-build

WORKDIR /app

# Create virtual environment
RUN python3 -m venv /app/venv

# Activate virtual environment and install Python dependencies
COPY requirements.txt ./
RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 3: Final Image
FROM python:3.11

WORKDIR /app

# Install PostgreSQL client tools (including pg_dump)
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from the build stage
COPY --from=python-build /app/venv /app/venv

# Copy frontend build files from the frontend-build stage
COPY --from=frontend-build /app/dist /app/dist

# Copy the rest of the project files
COPY . .

# List directory contents for debugging
RUN ls -al

# Activate virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Run the backup command (using .env for environment variables)
RUN python manage.py backup --output /app/backups/db_backup.dump

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Apply Django migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Clone images
RUN python manage.py process_thumbnails

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Remove the .env file to ensure it is not included in the final image
RUN rm /app/.env

# Display disk usage for debugging
RUN du -h --max-depth=5 | sort -rh

EXPOSE 8010

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Define the entry point for the container
CMD ["/app/venv/bin/gunicorn", "--config", "gunicorn_config.py", "myshop.wsgi:application"]