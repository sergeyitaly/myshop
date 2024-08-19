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
    }
}
