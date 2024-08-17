pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials-id')
        GITHUB_CREDENTIALS = credentials('github-credentials-id')
        DOCKER_IMAGE = credentials('dockerhub-image-id')
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
                    
                    // Build Docker image with ENV_ARGS passed as build arguments
                    def customImage = docker.build(
                        env.DOCKER_IMAGE, 
                        "--build-arg ENV_ARGS_FILE=/tmp/env_args.json -f Dockerfile ."
                    )

                    echo "Docker image built: ${env.DOCKER_IMAGE}"
                }
            }
        }

        stage('Run Django Commands') {
            steps {
                script {
                    echo "Running Django commands..."

                    // Use withCredentials to access the file
                    withCredentials([file(credentialsId: 'env-id', variable: 'ENV_ARGS_FILE')]) {
                        // Run commands inside Docker container
                        docker.image(env.DOCKER_IMAGE).inside {
                            // Install jq to process JSON
                            sh 'apt-get update && apt-get install -y jq'

                            // Copy the JSON file into the container
                            sh "cp ${ENV_ARGS_FILE} /tmp/env_args.json"

                            // Create .env file from JSON and run Django commands
                            sh """
                            jq -r 'to_entries | .[] | "\(.key)=\(.value)"' /tmp/env_args.json > .env
                            cat .env

                            python3 manage.py makemigrations
                            python3 manage.py migrate
                            python3 manage.py collectstatic --noinput
                            """

                            // Clean up frontend build files
                            sh 'rm -rf /app/frontend'
                            
                            // Display disk usage for debugging
                            sh 'du -h --max-depth=5 | sort -rh'

                            // Run Gunicorn to start the Django application
                            sh 'gunicorn myshop.wsgi:application --bind 0.0.0.0:8000 --workers 3'
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
                        docker.image(env.DOCKER_IMAGE).push()
                    }
                }
            }
        }
    }
}
