pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'docker.io'  // Replace with your registry URL if different
        DOCKER_BFLASK_IMAGE = 'my-flask-app:latest'
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
                    sh 'docker build -t my-flask-app .'
                    sh 'docker tag my-flask-app $DOCKER_BFLASK_IMAGE'
                }
            }
        }

        stage('Test Flask App') {
            steps {
                // Run tests for the Flask app
                sh 'docker run my-flask-app python -m pytest app/tests/'
            }
        }

        stage('Push Images to Registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_REGISTRY_CREDS}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    // Login to Docker registry
                    sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin $DOCKER_REGISTRY"

                    // Push Flask app image to registry
                    sh 'docker push $DOCKER_BFLASK_IMAGE'
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
                    sh 'docker run -p 5001:5001 -td $DOCKER_BFLASK_IMAGE'
                }
            }
        }
    }
}
