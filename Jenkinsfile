pipeline {
    agent any
    environment {
        VENV_DIR = "venv"
    }
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/bitsolutions4u/college_api.git'
            }
        }
        stage('Setup Python Environment') {
            steps {
                sh 'python3 -m venv $VENV_DIR'
                sh 'source $VENV_DIR/bin/activate'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Migrations') {
            steps {
                sh 'python manage.py makemigrations'
                sh 'python manage.py migrate'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'python manage.py test'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: '**/test-reports/*.xml', allowEmptyArchive: true
            junit 'test-reports/*.xml'
        }
    }
}