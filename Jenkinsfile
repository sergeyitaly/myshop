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
                        // Copy .env file for Docker build context
                        sh "cp ${ENV_ARGS_FILE} .env"

                        // Remove any old containers using the previous image
                        sh """
                        OLD_IMAGE_ID=\$(docker images -q ${DOCKER_IMAGE}:${TAG})
                        if [ ! -z "\$OLD_IMAGE_ID" ]; then
                            echo "Stopping and removing any containers using the old image..."
                            docker ps -a -q --filter ancestor=\$OLD_IMAGE_ID | xargs -r docker stop
                            docker ps -a -q --filter ancestor=\$OLD_IMAGE_ID | xargs -r docker rm
                        fi
                        """

                        // Remove the old Docker image with the same tag if it exists
                        sh """
                        if [ ! -z "\$OLD_IMAGE_ID" ]; then
                            echo "Removing old Docker image..."
                            docker rmi -f \$OLD_IMAGE_ID
                        fi
                        """

                        // Remove dangling images
                        sh """
                        DANGLING_IMAGES=\$(docker images -f "dangling=true" -q)
                        if [ ! -z "\$DANGLING_IMAGES" ]; then
                            echo "Removing dangling images..."
                            docker rmi -f \$DANGLING_IMAGES
                        fi
                        """

                        // Build the new Docker image with the specified tag
                        dockerImage = docker.build("${DOCKER_IMAGE}:${TAG}", "-f Dockerfile .")
                        echo "Docker image built: ${DOCKER_IMAGE}:${TAG}"

                        // Clean up the .env file after the build
                        sh "rm .env"
                        echo ".env is removed from the build context"
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
