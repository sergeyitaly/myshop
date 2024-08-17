pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials-id')
        GITHUB_CREDENTIALS = credentials('github-credentials-id')
        DOCKER_IMAGE = credentials('dockerhub-image-id')
        ENV_ARGS = credentials('env-id') // Ensure this is valid JSON
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
                    withCredentials([file(credentialsId: 'env-id', variable: 'ENV_ARGS_FILE')]) {
                        echo "Building Docker image..."

                        // Print ENV_ARGS for debugging
                        sh "cat ${ENV_ARGS_FILE} > env_args.json"
                        sh "cat env_args.json"

                        // Build Docker image
                        def customImage = docker.build(
                            env.DOCKER_IMAGE, 
                            "--build-arg ENV_ARGS='${ENV_ARGS_FILE}' -f Dockerfile ."
                        )
                        
                        echo "Docker image built: ${env.DOCKER_IMAGE}"
                    }
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
