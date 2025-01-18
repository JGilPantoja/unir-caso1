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
                    sh '''
                        if [ -f "${WORKSPACE}/unit_tests_executed.flag" ]; then
                            echo "Las pruebas unitarias ya se ejecutaron en este pipeline."
                            exit 1
                        fi

                        export PYTHONPATH=$(pwd)
                        pytest test/unit --junitxml=result-unit.xml
                        touch "${WORKSPACE}/unit_tests_executed.flag"
                    '''
                }
            }
        }
        stage('Static') {
            steps {
                sh '''
                flake8 --exit-zero --format=pylint app > flake8.out
                '''
                recordIssues(
                    tools: [flake8(name: 'Flake8', pattern: 'flake8.out')],
                    qualityGates: [
                        [threshold: 8, type: 'TOTAL', unstable: true],  
                        [threshold: 10, type: 'TOTAL', unstable: false] 
                    ]
                )
            }
        }

    }
}
