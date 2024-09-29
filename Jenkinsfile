pipeline {
    agent { 
        label 'Agent1'
    }
    
    environment {
        CONTAINER_NAME = 'Jenkins_master'
        DOCKER_IMAGE = 'devopsgoofy/weather-webapp'
        DOCKER_CREDENTIALS_ID = 'jenkins-dockerhub'
        EC2_USER = 'ubuntu'
        EC2_HOST = '3.66.157.23'
        SSH_CREDENTIALS_ID = 'your-ssh-credentials-id'
    }
	
    stages {
    	/*
    	stage("Clean") {
    		steps {
    			cleanWs()
    			docker stop -a
    		}
    	}
    	*/
    	stage("Checkout") {
    		steps {
    			checkout scm
    		}
    	}
    	
        stage('Install Dependencies') {
            steps {
                sh 'sudo apt update -y'
                sh 'sudo apt install python3-pip -y'
                sh 'sudo apt install pylint -y'
                sh 'sudo apt install jq -y'
            }
        }
        
       stage('Crete venv') {
            steps {
                sh '''
                    sudo apt install -y python3.12-venv
                    rm -rf webappvenv
                    python3 -m venv webappvenv
                    . webappvenv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pylint --fail-under=4 *.py
                    deactivate
                '''
            }

        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${env.DOCKER_IMAGE}")
                }
            }
        }
        /*
        stage('Check connectivity'){
            steps{
                sh '''
                    docker run --name smoke_test -d -p 5000:5000 devopsgoofy/weather-webapp
                    sleep 10
                    python3 ./app/smoke_test.py
                '''
            }
        }
        */
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${env.DOCKER_CREDENTIALS_ID}") {
                        docker.image("${env.DOCKER_IMAGE}").push('latest')
                    }
                }
            }
        }
        
        stage('Deploy to EC2') {
        	agent { label 'production' }
            steps {
                sh 'docker compose pull'
                sh 'docker compose up -d'
            }
        }
    }
    
    post {
        success {
            slackSend(channel: '#succeeded-build', color: 'good', message: "Build #${env.BUILD_NUMBER} succeeded.")
        }
        failure {
            slackSend(channel: '#devops-alerts', color: 'danger', message: "Build #${env.BUILD_NUMBER} failed.")
        }
    }
}
