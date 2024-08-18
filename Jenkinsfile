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

                        def customImage = docker.build(
                            DOCKER_IMAGE, "-f Dockerfile ."
                        )
                        echo "Docker image built: ${DOCKER_IMAGE}"
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing Docker image to Docker Hub..."
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        docker.image(DOCKER_IMAGE).push() // Adjust tag if needed
                    }
                }
            }
        }
    }
}
