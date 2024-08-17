pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials-id')
        GITHUB_CREDENTIALS = credentials('github-credentials-id')
        DOCKER_IMAGE = credentials('dockerhub-image-id')
        ENV_ARGS = credentials('env-id')
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
                    
                    // Fetch and escape ENV_ARGS
                    def envArgs = sh(script: 'echo "$ENV_ARGS"', returnStdout: true).trim()
                    envArgs = envArgs.replaceAll('\'', '\"') // Replace single quotes with double quotes
                    
                    // Build Docker image
                    def customImage = docker.build(
                        env.DOCKER_IMAGE, 
                        "--build-arg ENV_ARGS='${envArgs}' -f Dockerfile ."
                    )
                    
                    echo "Docker image built: ${env.DOCKER_IMAGE}"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing Docker image to Docker Hub..."
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        docker.image(env.DOCKER_IMAGE).push()
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
