pipeline {
    agent any

    environment {
        // Replace with your actual Docker Hub credentials ID
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials-id') 
        GITHUB_CREDENTIALS = credentials('github-credentials-id')
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

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing Docker image to Docker Hub..."
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        // Push the image with the tag from the build stage
                        dockerImage.push("${TAG}")
                    }
                }
            }
        }
    }
}
