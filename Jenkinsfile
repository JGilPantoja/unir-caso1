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
                        export PYTHONPATH=$(pwd)
                        /Users/javi/.local/bin/coverage run --branch --source=app --omit=app/__init__.py,app/api.py -m pytest test/unit
                        /Users/javi/.local/bin/coverage report
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
        stage('Coverage') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        export PYTHONPATH=$(pwd)
                        /Users/javi/.local/bin/coverage combine
                        /Users/javi/.local/bin/coverage xml
                    '''
                }
                cobertura coberturaReportFile: 'coverage.xml',
                          conditionalCoverageTargets: '90,80,80',
                          lineCoverageTargets: '95,85,90'
            }
        }

    }
}
