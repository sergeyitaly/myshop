# Stage 1: Build Frontend
FROM node:18 AS frontend-build

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Setup Python Environment and Install Dependencies
FROM python:3.11 AS python-build

WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Final Image
FROM python:3.11

WORKDIR /app

# Copy Python dependencies from the build stage
COPY --from=python-build /usr/local /usr/local

# Copy frontend build files from the frontend-build stage
COPY --from=frontend-build /app/frontend/dist /app/dist

# Copy the rest of the project files
COPY . .

# List directory contents for debugging
RUN ls -al

EXPOSE 8000

# Define the entry point for the container
CMD ["gunicorn", "myshop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
