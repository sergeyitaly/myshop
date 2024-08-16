pipeline {
    agent any

    environment {
        GITHUB_CREDENTIALS = credentials('github-token') // Use the ID you set in Jenkins
    }

    stages {

        stage('Perform GitHub API Operations') {
            steps {
                script {
                    def githubToken = env.GITHUB_CREDENTIALS
                    sh """
                    curl -H "Authorization: token ${githubToken}" https://api.github.com/repos/sergeyitaly/myshop
                    """
                }
            }
        }

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/sergeyitaly/myshop.git'
            }
        }
    stage('Load Environment Variables') {
        steps {
            script {
                withCredentials([string(credentialsId: '87f7447d-f83f-4552-a88c-1b0c235293c4', variable: 'ENV_CONTENT')]) {
                    writeFile file: '.env', text: ENV_CONTENT
                    def envVars = readFile('.env').trim().split('\n').collectEntries { line ->
                        def (key, value) = line.split('=')
                        [(key.trim()): value.trim()]
                    }
                    envVars.each { key, value -> env[key] = value }
                }
            }
        }
    }

        stage('Build Frontend') {
            steps {
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
                    docker.build(DOCKER_IMAGE, '-f Dockerfile .')
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        docker.image(DOCKER_IMAGE).push('latest')
                    }
                }
            }
        }

        stage('Deploy to AWS') {
            steps {
                withCredentials([
                    string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                    # Source environment variables from .env file
                    export $(grep -v '^#' .env | xargs)

                    cd frontend
                    npm run vercel-build
                    cd ..
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

        stage('Cleanup') {
            steps {
                sh 'rm -rf frontend'
                sh 'du -h --max-depth=5 | sort -rh'
            }
        }

        stage('Deploy Django Application') {
            steps {
                sh 'gunicorn myshop.wsgi:application --bind 0.0.0.0:8000 --workers 3'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
