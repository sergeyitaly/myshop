pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials-id')
        GITHUB_CREDENTIALS = credentials('github-credentials-id')
    }

    stages {
        stage('Perform GitHub API Operations') {
            steps {
                script {
                    echo "Fetching GitHub repository information..."
                    def githubToken = GITHUB_CREDENTIALS
                    sh """
                    curl -H "Authorization: token ${githubToken}" https://api.github.com/repos/sergeyitaly/myshop
                    """
                }
            }
        }

        stage('Checkout') {
            steps {
                script {
                    echo "Checking out the repository..."
                    git branch: 'main', url: 'https://github.com/sergeyitaly/myshop.git'
                }
            }
        }

        stage('Build Frontend') {
            steps {
                script {
                    dir('frontend') {
                        sh 'which docker || (echo "Docker not found, exiting..." && exit 1)'
                        sh 'docker --version'
                        sh 'docker pull node:18'
                    }
                }
                }
            }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    docker.build('mydockerimage', '-f Dockerfile .')
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing Docker image to Docker Hub..."
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        docker.image('mydockerimage').push('latest')
                    }
                }
            }
        }

        stage('Run Django Migrations and Collect Static') {
            steps {
                script {
                    echo "Running Django migrations and collecting static files..."
                    docker.image('mydockerimage').inside {
                        sh '''
                        export $(grep -v '^#' .env | xargs)
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        python3 manage.py makemigrations
                        python3 manage.py migrate
                        python3 manage.py compilemessages
                        pip install awscli
                        aws s3 mv media s3://kolorytmedia/media --recursive
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
