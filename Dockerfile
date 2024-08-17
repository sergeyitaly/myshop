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

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

EXPOSE 8000
