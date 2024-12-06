pipeline {
    agent any
    
    environment {
        PATH = "/opt/homebrew/bin:/Users/javi/.local/bin:${env.PATH}" 
    }

    stages {
        
        stage('getCode') {
            steps {
                git 'https://github.com/JGilPantoja/unir-caso1'
            }
        }
        
        stage('Build') {
            steps {
                echo 'NO HAY QUE COMPILAR NADA. ESTO ES PYTHON'
                sh "ls -la" 
                sh "pwd"
            }
        }

        stage('Tests') {
            parallel {
                stage('Unit') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                                export PYTHONPATH=$(pwd)
                                pytest test/unit --junitxml=result-unit.xml
                            '''
                        }
                    }
                }
                
                stage('Rest') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                                export FLASK_APP=app/api.py:api_application
                                nohup flask run --port=5000 > flask.log 2>&1 &
                                
                                nohup java -jar /usr/local/wiremock-standalone-3.10.0.jar --port 8081 --root-dir /Users/javi/Downloads/unir/unir-caso1/wiremock > wiremock.log 2>&1 &
                                
                                for i in {1..10}; do
                                    curl -s http://127.0.0.1:5000 > /dev/null && break
                                    sleep 1
                                done

                                for i in {1..10}; do
                                    curl -s http://127.0.0.1:8081/__admin > /dev/null && break
                                    sleep 1
                                done
                                
                                export PYTHONPATH=$(pwd)
                                pytest --junitxml=result-rest.xml test/rest
                                
                                pkill -f "flask run"
                                pkill -f "wiremock"
                            '''
                        }
                    }
                }
            }    
        }
        stage('Results') {
            steps {
                junit 'result-*.xml'
            }
        }       
        
}
}

