# Stage 1: Build Frontend
FROM node:18 AS frontend-build

WORKDIR /app/frontend
ENV VITE_API_BASE_URL=http://localhost:8010
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 1: Setup Python Environment and Install Dependencies
FROM python:3.11 AS python-build

WORKDIR /app

# Create virtual environment
RUN python3 -m venv /app/venv

# Activate virtual environment and install Python dependencies
COPY requirements.txt ./
RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt


# Stage 2: Build APK
FROM openjdk:11-jdk AS android-build

WORKDIR /app/android

# Install Android SDK and Gradle
RUN apt-get update && apt-get install -y wget unzip git
RUN wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O /cmdline-tools.zip \
    && mkdir -p /sdk/cmdline-tools \
    && unzip /cmdline-tools.zip -d /sdk/cmdline-tools \
    && mv /sdk/cmdline-tools/cmdline-tools /sdk/cmdline-tools/latest \
    && rm /cmdline-tools.zip
ENV ANDROID_HOME=/sdk
ENV PATH="$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools:$PATH"

# Accept SDK licenses and install build tools
RUN yes | sdkmanager --licenses \
    && sdkmanager --update \
    && sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.2"

# Copy Android project files
COPY android/ /app/android/

# Build APK
RUN ./gradlew assembleRelease

# Stage 3: Final Image
FROM python:3.11

WORKDIR /app

# Copy the virtual environment from the build stage
COPY --from=python-build /app/venv /app/venv

# Copy frontend build files from the frontend-build stage
COPY --from=frontend-build /app/dist /app/dist

# Copy APK from android-build stage
COPY --from=android-build /app/android/app/build/outputs/apk/release/app-release.apk /app/app-release.apk


# Copy the rest of the project files
COPY . .

# List directory contents for debugging
RUN ls -al

# Activate virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Apply Django migrations 
RUN python manage.py makemigrations
RUN python manage.py migrate

#clone images
RUN python manage.py process_thumbnails

#copy images
#COPY media /app/media

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
