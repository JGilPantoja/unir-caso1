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
                    rm -f ${WORKSPACE}/.coverage
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

                        if [ ! -f ".coverage" ]; then
                            echo "ERROR: Archivo .coverage no encontrado después de ejecutar coverage run."
                            exit 1
                        fi
                        /Users/javi/.local/bin/coverage report
                    '''
                }
                catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
                    junit 'result.xml' // Integra el plugin JUnit, pero ignora cualquier fallo o advertencia.
                }
                stash name: 'coverage-data', includes: '.coverage'
            }
        }

        stage('Coverage') {
            steps {
                unstash 'coverage-data'
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        export PYTHONPATH=$(pwd)
                        if [ ! -f ".coverage" ]; then
                            echo "ERROR: Archivo .coverage no encontrado después de unstash."
                            exit 1
                        fi
                        /Users/javi/.local/bin/coverage xml
                    '''
                }
                script {
                    try {
                        cobertura coberturaReportFile: 'coverage.xml',
                                  conditionalCoverageTargets: '100,0,80',
                                  lineCoverageTargets: '100,0,90'
                    } catch (Exception e) {
                        echo "Error al procesar el reporte de Cobertura: ${e.getMessage()}"
                    }
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
