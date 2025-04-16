pipeline {
    agent any

    environment {
        DOCKER_BFLASK_IMAGE = 'my-flask-app:latest'  // Local image tag
        DOCKER_REPO = 'lavanya986/my-flask-app'  // Docker Hub repository
    }

    stages {
        stage('Check and Stop Existing Containers') {
            steps {
                script {
                    // Check and stop any running container using port 5000 (MLflow)
                    def mlflowContainerId = sh(script: "docker ps --filter 'publish=5000' --format '{{.ID}}'", returnStdout: true).trim()
                    if (mlflowContainerId) {
                        // Stop the MLflow container
                        sh "docker stop ${mlflowContainerId}"
                        echo "Stopped MLflow container ${mlflowContainerId} using port 5000"
                    } else {
                        echo "No MLflow container found using port 5000."
                    }

                    // Check and stop any running container using port 5001 (Flask)
                    def flaskContainerId = sh(script: "docker ps --filter 'publish=5001' --format '{{.ID}}'", returnStdout: true).trim()
                    if (flaskContainerId) {
                        // Stop the Flask container
                        sh "docker stop ${flaskContainerId}"
                        echo "Stopped Flask container ${flaskContainerId} using port 5001"
                    } else {
                        echo "No Flask container found using port 5001."
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

        stage('Deploy Containers') {
            steps {
                script {
                    // Run MLflow container on port 5000
                    echo "Starting MLflow container..."
                    sh 'docker run -p 5000:5000 -td mlflow-app'

                    // Run Flask container on port 5001
                    echo "Starting Flask container..."
                    sh 'docker run -p 5001:5001 -td $DOCKER_REPO:latest'
                }
            }
        }
    }
}
