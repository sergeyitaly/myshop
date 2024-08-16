pipeline {
    agent any

    environment {
        GITHUB_CREDENTIALS = credentials('github-token')
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
    }

    stages {
        stage('Perform GitHub API Operations') {
            steps {
                script {
                    echo "Fetching GitHub repository information..."
                    def githubToken = env.GITHUB_CREDENTIALS
                    sh """
                    curl -H "Authorization: token ${githubToken}" https://api.github.com/repos/sergeyitaly/myshop
                    """
                }
            }
        }

        stage('Checkout') {
            steps {
                echo "Checking out the Git repository..."
                git branch: 'main', url: 'https://github.com/sergeyitaly/myshop.git'
            }
        }

        stage('Load Environment Variables') {
            steps {
                script {
                    echo "Loading environment variables..."
                    withCredentials([string(credentialsId: '87f7447d-f83f-4552-a88c-1b0c235293c4', variable: 'ENV_CONTENT')]) {
                        writeFile file: '.env', text: ENV_CONTENT
                        def envVars = readFile('.env').trim().split('\n').collectEntries { line ->
                            def (key, value) = line.split('=')
                            [(key.trim()): value.trim()]
                        }
                        envVars.each { key, value -> env[key] = value }
                    }
                    echo "Environment variables loaded:"
                    sh 'cat .env'
                }
            }
        }

        stage('Build Frontend') {
            steps {
                echo "Building frontend..."
                dir('frontend') {
                    sh 'npm install'
                    sh 'npm run vercel-build'
                    sh 'npm audit fix'
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
                        python3 manage.py collectstatic --noinput --clear
                        '''
                    }
                }
            }
        }

        stage('Cleanup') {
            steps {
                echo "Cleaning up..."
                sh 'rm -rf frontend'
                sh 'du -h --max-depth=5 | sort -rh'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
