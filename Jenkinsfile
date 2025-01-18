pipeline {
    agent any

    environment {
        PATH = "/opt/homebrew/bin:/Users/javi/.local/bin:${env.PATH}" 
    }

    stages {
        stage('getCode') {
            steps {
                sh '''
                    whoami
                    hostname
                    echo ${WORKSPACE}
                '''
                git branch: 'master', url: 'https://github.com/JGilPantoja/unir-caso1'
            }
        }
        
        stage('Build') {
            steps {
                sh '''
                    whoami
                    hostname
                    echo ${WORKSPACE}
                '''
                unstash 'source'
                echo 'NO HAY QUE COMPILAR NADA. ESTO ES PYTHON'
                sh "ls -la" 
                sh "pwd"
                
            }
        }

        stage('Tests') {
            parallel {
                stage('Unit') {
                    steps {
                        sh '''
                            whoami
                            hostname
                            echo ${WORKSPACE}
                        '''
                        unstash 'source'
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                                export PYTHONPATH=$(pwd)
                                pytest test/unit --junitxml=result-unit.xml
                            '''
                            stash includes: 'result-unit.xml', name: 'unit-results'
                        }
                        
                    }
                }
                
                stage('Rest') {
                    steps {
                        sh '''
                            whoami
                            hostname
                            echo ${WORKSPACE}
                        '''
                        unstash 'source'
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                                    
                                flaskPort=$((5000 + RANDOM % 1000))
                                mockPort=$((8081 + RANDOM % 1000))
                                export FLASK_PORT=${flaskPort}
                                export MOCK_PORT=${mockPort}

                                export FLASK_APP=app/api.py:api_application
                                nohup flask run --port=${FLASK_PORT} > flask.log 2>&1 &
                                
                                nohup java -jar /usr/local/wiremock-standalone-3.10.0.jar --port=${MOCK_PORT} --root-dir /path/to/wiremock > wiremock.log 2>&1 &
                                
                                for i in {1..10}; do
                                    curl -s http://127.0.0.1:${FLASK_PORT} > /dev/null && break
                                    sleep 1
                                done

                                for i in {1..10}; do
                                    curl -s http://127.0.0.1:${MOCK_PORT}/__admin > /dev/null && break
                                    sleep 1
                                done
                                
                                export PYTHONPATH=$(pwd)
                                pytest --junitxml=result-rest.xml test/rest
                                
                                pkill -f "flask run"
                                pkill -f "wiremock"
                            '''
                            stash includes: 'result-rest.xml', name: 'rest-results'
                        }
                        
                    }
                }
            }    
        }
        
        stage('Results') {
            steps {
                sh '''
                    whoami
                    hostname
                    echo ${WORKSPACE}
                '''
                unstash 'unit-results'
                unstash 'rest-results'
                junit 'result-*.xml'
                
            }
        }
    }
}
