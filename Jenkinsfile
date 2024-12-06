pipeline {
    agent none

    environment {
        PATH = "/opt/homebrew/bin:/Users/javi/.local/bin:${env.PATH}" 
    }

    stages {
        stage('getCode') {
            agent { label 'master' }
            steps {
                git 'https://github.com/JGilPantoja/unir-caso1'
                sh 'whoami'
                stash includes: '**', name: 'code'
            }
        }

        stage('Build') {
            agent { label 'master' }
            steps {
                unstash 'code'
                sh 'whoami'
                sh "ls -la"
            }
        }

        stage('Tests') {
            parallel {
                stage('Unit') {
                    agent { label 'agent1' }
                    steps {
                        unstash 'code'
                        sh 'whoami'
                        sh '''
                            export PYTHONPATH=$(pwd)
                            pytest test/unit --junitxml=result-unit.xml
                        '''
                        stash includes: 'result-unit.xml', name: 'unit-results'
                        deleteDir() 
                    }
                }

                stage('Rest') {
                    agent { label 'agent2' }
                    steps {
                        unstash 'code'
                        sh 'whoami'
                        sh '''
                            export FLASK_APP=app/api.py:api_application
                            nohup flask run --port=5000 > flask.log 2>&1 &
                            nohup java -jar /usr/local/wiremock-standalone-3.10.0.jar --port 8081 --root-dir /Users/javi/Downloads/unir/unir-caso1/wiremock > wiremock.log 2>&1 &
                            pytest test/rest --junitxml=result-rest.xml
                            pkill -f "flask run"
                            pkill -f "wiremock"
                        '''
                        stash includes: 'result-rest.xml', name: 'rest-results'
                        deleteDir() // Limpieza del workspace
                    }
                }
            }
        }

        stage('Results') {
            agent { label 'master' }
            steps {
                echo 'Procesando resultados en el nodo principal'
                unstash 'unit-results'
                unstash 'rest-results'
                sh 'whoami'
                junit 'result-*.xml'
                deleteDir() // Limpieza del workspace
            }
        }
    }
}

