pipeline {
    agent any

    environment {
        DOCKER_BFLASK_IMAGE = 'my-flask-app:latest'  // Local image tag
        DOCKER_REPO = 'lavanya986/my-flask-app'  // Docker Hub repository
    }

    stages {
        stage('Check and Stop Existing Container') {
            steps {
                script {
                    def containerId = sh(script: "docker ps --filter 'publish=5000' --format '{{.ID}}'", returnStdout: true).trim()

                    if (containerId) {
                        // Stop the container
                        sh "docker stop ${containerId}"
                        echo "Stopped container ${containerId} that was using port 5000"

                        // Verify the container is stopped
                        def containerRunning = sh(script: "docker ps --filter 'id=${containerId}' --format '{{.ID}}'", returnStdout: true).trim()

                        if (containerRunning) {
                            error "Failed to stop container ${containerId}. Manual intervention required."
                        } else {
                            echo "Container ${containerId} successfully stopped."
                        }
                    } else {
                        echo "No container found using port 5000."
                    }
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    // Build Flask app image
                    sh 'docker build -t $DOCKER_BFLASK_IMAGE .'
                    
                    // Tag the image for Docker Hub repository (lavanya986/my-flask-app)
                    sh 'docker tag $DOCKER_BFLASK_IMAGE $DOCKER_REPO:latest'
                }
            }
        }

        stage('Test Flask App') {
            steps {
                // Run tests for the Flask app
                sh 'docker run $DOCKER_BFLASK_IMAGE python -m pytest app/tests/'
            }
        }

        stage('Push Images to Registry') {
            steps {
                script {
                    // Hardcoded Docker credentials
                    def dockerUsername = "lavanya986"
                    def dockerPassword = "Lavanya@26"
                    def dockerRegistry = "docker.io"  // Docker Hub registry

                    // Login to Docker registry with hardcoded credentials
                    sh "echo $dockerPassword | docker login -u $dockerUsername --password-stdin $dockerRegistry"

                    // Push Flask app image to registry (use the tagged repository)
                    sh 'docker push $DOCKER_REPO:latest'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh 'docker run -p 5000:5000 -td $DOCKER_BFLASK_IMAGE'
                }
            }
        }
    }
}
