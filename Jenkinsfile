pipeline {
    agent any

    environment {
        PATH = "/opt/homebrew/bin:/Users/javi/.local/bin:/Users/javi/Downloads/unir/apache-jmeter-5.6.3/bin:${env.PATH}" 
        FLASK_PORT = "5000"
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
                sh 'cp /Users/javi/Downloads/unir/apache-jmeter-5.6.3/bin/test-plan.jmx ${WORKSPACE}/test-plan.jmx'
            }
        }
        
        stage('Unit') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        export PYTHONPATH=$(pwd)
                        /Users/javi/.local/bin/coverage run --branch --source=app --omit=app/__init__.py,app/api.py -m pytest --junitxml=result-unit.xml test/unit

                        if [ ! -f ".coverage" ]; then
                            echo "ERROR: Archivo .coverage no encontrado después de ejecutar coverage run."
                            exit 1
                        fi
                        if [ ! -f "result-unit.xml" ]; then
                            echo "ERROR: Archivo result-unit.xml no encontrado después de ejecutar pytest."
                            exit 1
                        fi
                        /Users/javi/.local/bin/coverage xml
                    '''
                }
                junit 'result-unit.xml'
            }
        }

        stage('Coverage') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
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
        stage('Security') {
            steps {
                sh '''
                bandit --exit-zero -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}] {msg}"
                '''
                recordIssues(
                    tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')],
                    qualityGates: [
                        [threshold: 2, type: 'TOTAL', unstable: true],  
                        [threshold: 4, type: 'TOTAL', unstable: false] 
                    ]
                )
            }
        }
        stage('Performance') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        export FLASK_PORT=${FLASK_PORT}
                        export FLASK_APP=app/api.py:api_application

                        nohup flask run --port=${FLASK_PORT} > flask.log 2>&1 &

                        for i in {1..10}; do
                            curl -s http://127.0.0.1:${FLASK_PORT} > /dev/null && break
                            sleep 1
                        done

                        jmeter -n -t test-plan.jmx -l results.jtl

                        pkill -f "flask run"
                    '''
                }
                
                script {
                    publishPerformanceReport parsers: [jmeterParser(pattern: 'results.jtl')]
                }
            }
        }
    }
}
