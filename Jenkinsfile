pipeline {
    agent any

    environment {
        GITHUB_CREDENTIALS = credentials('github-credentials-id') // Your GitHub credentials ID
        DOCKER_IMAGE = 'sergeyitaly/koloryt' // Base Docker image name without tag
        TAG = 'serhii_test' // Tag for your Docker image
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    deleteDir()
                    echo "Workspace is deleted..."
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
                    withCredentials([file(credentialsId: 'env-id', variable: 'ENV_ARGS_FILE')]) {
                        sh "cp ${ENV_ARGS_FILE} .env"
                        // Build Docker image with tag
                        dockerImage = docker.build("${DOCKER_IMAGE}:${TAG}", "-f Dockerfile .")
                        echo "Docker image built: ${DOCKER_IMAGE}:${TAG}"
                    }
                }
            }
        }

        stage('Docker Push') {
            agent any
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials-id', passwordVariable: 'dockerHubPassword', usernameVariable: 'dockerHubUser')]) {
                    script {
                        echo "Logging into Docker Hub..."
                        sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPassword}"
                        echo "Pushing Docker image to Docker Hub..."
                        sh "docker push ${DOCKER_IMAGE}:${TAG}"
                    }
                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                script {
                    echo "Deploying with Docker Compose..."
                    // Define a docker-compose.yml file content as a string
                    def dockerComposeYaml = """
                    version: '3.8'
                    services:
                      web:
                        image: ${DOCKER_IMAGE}:${TAG}
                        container_name: django_web
                        command: gunicorn myshop.wsgi:application --bind 0.0.0.0:8000 --workers 3
                        ports:
                          - "8000:8000"
                        volumes:
                          - .:/app
                        depends_on:
                          - redis
                        environment:
                          - DJANGO_SETTINGS_MODULE=myshop.settings
                          - REDIS_URL=redis://redis:6379/1

                      redis:
                        image: redis:alpine
                        container_name: redis

                      celery:
                        image: ${DOCKER_IMAGE}:${TAG}
                        container_name: django_celery
                        command: celery -A myshop worker --loglevel=info
                        depends_on:
                          - redis
                        environment:
                          - DJANGO_SETTINGS_MODULE=myshop.settings
                          - REDIS_URL=redis://redis:6379/1

                      celery-beat:
                        image: ${DOCKER_IMAGE}:${TAG}
                        container_name: django_celery_beat
                        command: celery -A myshop beat --loglevel=info
                        depends_on:
                          - redis
                        environment:
                          - DJANGO_SETTINGS_MODULE=myshop.settings
                          - REDIS_URL=redis://redis:6379/1
                    """

                    // Write docker-compose.yml file
                    writeFile file: 'docker-compose.yml', text: dockerComposeYaml

                    // Run Docker Compose
                    sh "docker-compose up -d"
                }
            }
        }
    }



    }
}
