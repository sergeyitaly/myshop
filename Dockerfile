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

# Create virtual environment
RUN python3 -m venv /app/venv

# Activate virtual environment and install Python dependencies
COPY requirements.txt ./
RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 3: Final Image
FROM python:3.11

WORKDIR /app

# Copy the virtual environment from the build stage
COPY --from=python-build /app/venv /app/venv

# Copy frontend build files from the frontend-build stage
COPY --from=frontend-build /app/frontend/dist /app/dist

# Copy the rest of the project files
COPY . .

# List directory contents for debugging
RUN ls -al

# Activate virtual environment and run Django commands
ENV PATH="/app/venv/bin:$PATH"

EXPOSE 8000

# Define the entry point for the container
CMD ["gunicorn", "myshop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
