pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials-id')
        GITHUB_CREDENTIALS = credentials('github-credentials-id')
        DOCKER_IMAGE = credentials('dockerhub-image-id') // Replace with the actual Docker image name
    }

    stages {
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
                    def customImage = docker.build(
                        "${DOCKER_IMAGE}", " -f Dockerfile ."
                    )
                    echo "Docker image built: ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Run Django Commands') {
            steps {
                script {
                    echo "Running Django commands..."
                    withCredentials([file(credentialsId: 'env-id', variable: 'ENV_ARGS_FILE')]) {
                        docker.image("${DOCKER_IMAGE}").inside {
                            sh "cp ${ENV_ARGS_FILE} .env"
                            sh """
                            cat .env
                            python manage.py makemigrations
                            python manage.py migrate
                            python manage.py collectstatic --noinput
                            """
                            // Display disk usage for debugging
                            sh 'du -h --max-depth=5 | sort -rh'
                        }
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing Docker image to Docker Hub..."
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        docker.image("${DOCKER_IMAGE}").push('latest') // Adjust tag if needed
                    }
                }
            }
        }
    }
}
