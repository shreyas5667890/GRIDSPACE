pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/shreyas5667890/GRIDSPACE.git'
                 
            }
        }

        stage('Setup') {
            steps {
                bat 'python -m venv .venv'
                bat '.venv\\Scripts\\python -m pip install --upgrade pip'
                bat '.venv\\Scripts\\python -m pip install -r requirements.txt'
            }
        }

        stage('Run App') {
            steps {
                bat 'cd gridspace && ..\\.venv\\Scripts\\python main.py'
            }
        }
    }
}
