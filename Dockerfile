# Stage 1: Build Frontend
FROM node:18 AS frontend-build

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Setup Python Environment
FROM python:3.11

WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend build files from the previous stage
COPY --from=frontend-build /app/dist /app/frontend/dist

# Copy all project files
COPY . .

EXPOSE 8000

# Define the entry point for the container
CMD ["gunicorn", "myshop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
