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
        
        stage('Unit') {
            steps {
                sh '''
                    whoami
                    hostname
                    echo ${WORKSPACE}
                '''
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    # Verificar si ya se ejecutaron
                    if [ -f ${WORKSPACE}/unit_tests_executed.flag ]; then
                        echo "Las pruebas unitarias ya se ejecutaron en este pipeline."
                        exit 1
                    fi

                    # Ejecutar las pruebas unitarias y marcar como ejecutado
                    export PYTHONPATH=$(pwd)
                    pytest test/unit --junitxml=result-unit.xml
                    touch ${WORKSPACE}/unit_tests_executed.flag
                }
            }
        }
    }
}
