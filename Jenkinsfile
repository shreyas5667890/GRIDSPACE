pipeline {
    agent any

    stages {

        stage('Checkout Repo') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/shreyas5667890/GRIDSPACE.git'
            }
        }

        stage('Start Preview Server') {
            steps {
                bat '''
                cd Gridspace
                start /B "" "C:\\Users\\Shreyas\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m http.server 8000
                '''
            }
        }

    }
}
