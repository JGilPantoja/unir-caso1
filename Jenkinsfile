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
                    # Eliminar archivos residuales de cobertura
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
                        /Users/javi/.local/bin/coverage report
                    '''
                }
                archiveArtifacts artifacts: '.coverage', allowEmptyArchive: true
            }
        }

        stage('Static') {
            steps {
                sh '''
                # Ejecutar análisis de código estático con Flake8
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
                unstash 'coverage-data'
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        export PYTHONPATH=$(pwd)
                        # Verificar y combinar datos de cobertura
                        if [ -f "${WORKSPACE}/.coverage" ]; then
                            /Users/javi/.local/bin/coverage combine
                            /Users/javi/.local/bin/coverage xml
                        else
                            echo "No coverage data found to combine."
                            exit 1
                        fi
                    '''
                }
                cobertura coberturaReportFile: 'coverage.xml',
                          conditionalCoverageTargets: '90,80,80',
                          lineCoverageTargets: '95,85,90'
            }
        }
    }
}
