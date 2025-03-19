// pipeline {
//     agent any
// //     environment {
// //         VENV_DIR = "venv"
// //     }
//     stages {
//         stage('Clone Repository') {
//             steps {
//                 git 'https://github.com/bitsolutions4u/college_api.git', branch: 'master'
//             }
//         }
//         stage('Install System Dependencies') {
//             steps {
//                 script {
//                     try {
//                         sh 'sudo apt-get update -y'
//                     } catch (Exception e) {
//                         echo "Failed to update package list: ${e.getMessage()}"
//                         error "Stopping pipeline due to failure in 'Install System Dependencies' stage."
//                     }
//                 }
//             }
//         }
//         stage('Setup Python Environment') {
//             steps {
//                 script {
//                     try {
//                         sh 'sudo apt-get install -y python3 python3-pip'
//                     } catch (Exception e) {
//                         echo "Failed to install Python: ${e.getMessage()}"
//                         error "Stopping pipeline due to failure in 'Setup Python Environment' stage."
//                     }
//                 }
//             }
//         }
//         stage('Install Dependencies') {
//             steps {
//                 script {
//                     try {
//                         sh 'pip3 install -r requirements.txt'
//                     } catch (Exception e) {
//                         echo "Failed to install Python dependencies: ${e.getMessage()}"
//                         error "Stopping pipeline due to failure in 'Install Dependencies' stage."
//                     }
//                 }
//             }
//         }
//         stage('Run Migrations') {
//             steps {
//                 script {
//                       try {
//                         sh 'python3 manage.py makemigrations'
//                     } catch (Exception e) {
//                         echo "Failed to run migrations: ${e.getMessage()}"
//                         error "Stopping pipeline due to failure in 'Run Migrations' Makemigrations stage."
//                     }
//                     try {
//                         sh 'python3 manage.py migrate'
//                     } catch (Exception e) {
//                         echo "Failed to run migrations: ${e.getMessage()}"
//                         error "Stopping pipeline due to failure in 'Run Migrations' migrate stage."
//                     }
//                 }
//             }
//         }
//         stage('Run Tests') {
//             steps {
//                 script {
//                     try {
//                         sh 'python3 manage.py test'
//                     } catch (Exception e) {
//                         echo "Failed to run tests: ${e.getMessage()}"
//                         error "Stopping pipeline due to failure in 'Run Tests' stage."
//                     }
//                 }
//             }
//         }
//     }
//
//    post {
//         always {
//             archiveArtifacts artifacts: '**/target/*.jar', allowEmptyArchive: true
//             junit '**/target/test-*.xml'
//         }
//         failure {
//             mail to: 'bitsolutions4u@gmail.com',
//                  subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
//                  body: "Something is wrong with ${env.JOB_NAME}. Please investigate."
//         }
//     }
// }


pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/college_api.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t django-app .'
            }
        }

        stage('Stop & Remove Old Container') {
            steps {
                sh 'docker stop django-app || true'
                sh 'docker rm django-app || true'
            }
        }

        stage('Run New Container') {
            steps {
                sh 'docker run -d -p 8000:8000 --name django-app django-app'
            }
        }
    }
}
