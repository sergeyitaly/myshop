pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials-id')
        GITHUB_CREDENTIALS = credentials('github-credentials-id')
        DOCKER_IMAGE = 'custom-jenkins:latest'
    }

    stages {
        stage('Perform GitHub API Operations') {
            steps {
                script {
                    echo "Fetching GitHub repository information..."
                    sh """
                    curl -H "Authorization: token ${GITHUB_CREDENTIALS_PSW}" https://api.github.com/repos/sergeyitaly/myshop || { echo "Failed to fetch GitHub repository information"; exit 1; }
                    """
                }
            }
        }

        stage('Checkout') {
            steps {
                script {
                    echo "Checking out the repository..."
                    git branch: 'main', credentialsId: 'github-credentials-id', url: 'https://github.com/sergeyitaly/myshop.git'
                    sh "ls -lat"
                }
            }
        }

        stage('Build Docker Image') {
            agent {
                docker {
                    image 'custom-jenkins:latest'
                    args '-u root'
                }
            }
            steps {
                script {
                    withCredentials([file(credentialsId: 'env-id', variable: 'ENV_ARGS_FILE')]) {
                        echo "Building Docker image..."
                        
                        sh "cp ${ENV_ARGS_FILE} /tmp/env_args.json"
                        sh "cat /tmp/env_args.json"

                        def customImage = docker.build(
                            env.DOCKER_IMAGE, 
                            "--build-arg ENV_ARGS_FILE=/tmp/env_args.json -f Dockerfile ."
                        )
                                            
                        sh "ls -lat"
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
