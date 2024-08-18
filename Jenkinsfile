pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials-id')
        GITHUB_CREDENTIALS = credentials('github-credentials-id')
        DOCKER_IMAGE = 'sergeyitaly/koloryt' // Base Docker image name, without tag
        REGISTRY = 'sergeyitaly/koloryt' // Base registry name
        REGISTRY_CREDENTIAL = 'dockerhub-credentials-id' // Docker Hub credentials ID
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
                        // Specify the Dockerfile explicitly and use the current directory as the context
                        dockerImage = docker.build(
                            "${DOCKER_IMAGE}:${BUILD_NUMBER}",
                            "-f Dockerfile ." // Dockerfile location and build context
                        )
                        echo "Docker image built: ${dockerImage.imageName()}"
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing Docker image to Docker Hub..."
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        dockerImage.push() // Push the image with the tag from the build stage
                    }
                }
            }
        }
    }
}
