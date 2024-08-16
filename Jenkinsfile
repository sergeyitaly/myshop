pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials-id')
        GITHUB_CREDENTIALS = credentials('github-credentials-id')
        ENV_FILE = credentials('87f7447d-f83f-4552-a88c-1b0c235293c4') // Securely load the .env file
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

        stage('Build Docker Image on Remote Server') {
            steps {
                script {
                    echo "Building Docker image on remote server..."
                    docker.withServer('tcp://swarm.example.com:2376', 'swarm-certs') { // Replace with your server's details
                        def customImage = docker.build('mydockerimage', '-f Dockerfile .')
                    }
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
                        // Create .env file with credentials loaded from Jenkins
                        writeFile file: '.env', text: ENV_FILE

                        sh '''
                        # Load environment variables from .env file
                        export $(grep -v '^#' .env | xargs)
                        
                        # Install required Python packages
                        pip install --upgrade pip
                        pip install -r requirements.txt

                        # Run Django migrations
                        python3 manage.py makemigrations
                        python3 manage.py migrate

                        # Compile message files
                        python3 manage.py compilemessages

                        # Install AWS CLI and upload media files
                        pip install awscli
                        aws s3 mv media s3://kolorytmedia/media --recursive

                        # Collect static files
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
