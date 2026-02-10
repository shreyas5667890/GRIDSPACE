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
                bat '"C:\\Users\\Shreyas\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m venv .venv'
                bat '.venv\\Scripts\\python -m pip install --upgrade pip'
            }
        }

        stage('Run App') {
            steps {
                bat 'cd gridspace && ..\\.venv\\Scripts\\python main.py'
            }
        }
    }
}
