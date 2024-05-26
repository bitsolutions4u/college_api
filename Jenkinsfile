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
         stage('Install System Dependencies') {
            steps {
                sh '''
                sudo apt-get update
                sudo apt-get install -y python3-venv
                '''
            }
        }
        stage('Setup Python Environment') {
            steps {
                sh 'python3 -m venv ${VENV_DIR}'
                sh 'source ${VENV_DIR}/bin/activate'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'source ${VENV_DIR}/bin/activate'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Migrations') {
            steps {
                sh 'source ${VENV_DIR}/bin/activate'
                sh 'python manage.py makemigrations'
                sh 'python manage.py migrate'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'source ${VENV_DIR}/bin/activate'
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