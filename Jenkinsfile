pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials-id')
        GITHUB_CREDENTIALS = credentials('github-credentials-id')
        DEBUG = credentials('debug-id')
        SECRET_KEY = credentials('secret-key-id')
        ALLOWED_HOSTS = credentials('allowed-hosts-id')
 //       AWS_S3_REGION_NAME = credentials('aws-s3-region-id')
 //       AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
 //       AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key-id')
  //      AWS_STORAGE_BUCKET_NAME = credentials('aws-storage-bucket-id')
  //      USE_S3 = credentials('use-s3-id')
  //      AWS_MEDIA = credentials('aws-media-id')
  //      REDIS_CACHE_LOCATION = credentials('redis-cache-location-id')
  //      REDIS_BROKER_URL = credentials('redis-broker-url-id')
  //      AWS_STATIC_LOCATION = credentials('aws-static-location-id')
  //      EMAIL_HOST_USER = credentials('email-host-user-id')
  //      EMAIL_HOST_PASSWORD = credentials('email-host-password-id')
   //     VERCEL_FORCE_NO_BUILD_CACHE = credentials('vercel-force-no-build-cache-id')
    //    VERCEL_DOMAIN = credentials('vercel-domain-id')
   //     LOCAL_HOST = credentials('local-host-id')
   //     MAILGUN_SENDER_DOMAIN = credentials('mailgun-sender-domain-id')
   //     MAILGUN_API_KEY = credentials('mailgun-api-key-id')
  //      MAILGUN_SMTP_USERNAME = credentials('mailgun-smtp-username-id')
  //      MAILGUN_PASSWORD = credentials('mailgun-password-id')
   //     NOTIFICATIONS_API = credentials('notifications-api-id')
    //    CLOUDFARE_TOKEN = credentials('cloudfare-token-id')
   //     DB_PASSWORD = credentials('db-password-id')
   //     DB_URL = credentials('db-url-id')
   //     POSTGRES_DATABASE = credentials('postgres-database-id')
   //     POSTGRES_USER = credentials('postgres-user-id')
   //     POSTGRES_PASSWORD = credentials('postgres-password-id')
   //     POSTGRES_HOST = credentials('postgres-host-id')
   //     POSTGRES_PORT = credentials('postgres-port-id')
   //     VITE_API_BASE_URL = credentials('vite-api-base-url-id')
          DOCKER_IMAGE = "docker.io/sergeyitaly/koloryt:${BUILD_ID}" // Define Docker image
    }

    stages {
        stage('Perform GitHub API Operations') {
            steps {
                script {
                    echo "Fetching GitHub repository information..."
                    sh """
                    curl -H "Authorization: token ${GITHUB_CREDENTIALS}" https://api.github.com/repos/sergeyitaly/myshop
                    """
                }
            }
        }

        stage('Checkout') {
            steps {
                script {
                    echo "Checking out the repository..."
                    git branch: 'main', credentialsId: GITHUB_CREDENTIALS, url: 'https://github.com/sergeyitaly/myshop.git'
                    sh "ls -lat"

                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    def customImage = docker.build(env.DOCKER_IMAGE, '-f Dockerfile .')
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing Docker image to Docker Hub..."
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        docker.image(env.DOCKER_IMAGE).push('latest')
                    }
                }
            }
        }

        stage('Run Django Migrations and Collect Static') {
            steps {
                script {
                    echo "Running Django migrations and collecting static files..."
                    docker.image(env.DOCKER_IMAGE).inside {
                        sh '''
                        # Write environment variables to .env file
                        echo "DEBUG=${DEBUG}" > .env
                        echo "SECRET_KEY=${SECRET_KEY}" >> .env
                        echo "ALLOWED_HOSTS=${ALLOWED_HOSTS}" >> .env
                        echo "AWS_S3_REGION_NAME=${AWS_S3_REGION_NAME}" >> .env
                        echo "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}" >> .env
                        echo "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}" >> .env
                        echo "AWS_STORAGE_BUCKET_NAME=${AWS_STORAGE_BUCKET_NAME}" >> .env
                        echo "USE_S3=${USE_S3}" >> .env
                        echo "AWS_MEDIA=${AWS_MEDIA}" >> .env
                        echo "REDIS_CACHE_LOCATION=${REDIS_CACHE_LOCATION}" >> .env
                        echo "REDIS_BROKER_URL=${REDIS_BROKER_URL}" >> .env
                        echo "AWS_STATIC_LOCATION=${AWS_STATIC_LOCATION}" >> .env
                        echo "EMAIL_HOST_USER=${EMAIL_HOST_USER}" >> .env
                        echo "EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}" >> .env
                        echo "VERCEL_FORCE_NO_BUILD_CACHE=${VERCEL_FORCE_NO_BUILD_CACHE}" >> .env
                        echo "VERCEL_DOMAIN=${VERCEL_DOMAIN}" >> .env
                        echo "LOCAL_HOST=${LOCAL_HOST}" >> .env
                        echo "MAILGUN_SENDER_DOMAIN=${MAILGUN_SENDER_DOMAIN}" >> .env
                        echo "MAILGUN_API_KEY=${MAILGUN_API_KEY}" >> .env
                        echo "MAILGUN_SMTP_USERNAME=${MAILGUN_SMTP_USERNAME}" >> .env
                        echo "MAILGUN_PASSWORD=${MAILGUN_PASSWORD}" >> .env
                        echo "NOTIFICATIONS_API=${NOTIFICATIONS_API}" >> .env
                        echo "CLOUDFARE_TOKEN=${CLOUDFARE_TOKEN}" >> .env
                        echo "DB_PASSWORD=${DB_PASSWORD}" >> .env
                        echo "DB_URL=${DB_URL}" >> .env
                        echo "POSTGRES_DATABASE=${POSTGRES_DATABASE}" >> .env
                        echo "POSTGRES_USER=${POSTGRES_USER}" >> .env
                        echo "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}" >> .env
                        echo "POSTGRES_HOST=${POSTGRES_HOST}" >> .env
                        echo "POSTGRES_PORT=${POSTGRES_PORT}" >> .env
                        echo "VITE_API_BASE_URL=${VITE_API_BASE_URL}" >> .env

                        # Install required Python packages
                        pip install --upgrade pip
                        pip install -r requirements.txt

                        # Run Django migrations
                        python3 manage.py makemigrations
                        python3 manage.py migrate

                        # Compile message files
                        python3 manage.py compilemessages

                        # Install AWS CLI and upload media files
                        pip install awscli
                        aws s3 mv media s3://kolorytmedia/media --recursive

                        # Collect static files
                        python3 manage.py collectstatic --noinput --clear
                        '''
                    }
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    echo "Cleaning up..."
                    sh 'rm -rf frontend'
                    sh 'du -h --max-depth=5 | sort -rh'
                }
            }
        }
    }
}
