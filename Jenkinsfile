pipeline {
    agent any

    environment {
        IMAGE_NAME = "gridspace-app"
        CONTAINER_NAME = "gridspace-container"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build --no-cache -t $IMAGE_NAME .'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker rm -f $CONTAINER_NAME || true
                docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME
                '''
            }
        }
    }
}