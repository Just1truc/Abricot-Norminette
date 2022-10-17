pipeline {
  agent {
    docker {
      image 'python:bullseye'
    }
  }
  stages {
    stage('Env. info') {
      parallel {
        stage('Env. info') {
          steps {
            sh 'python -V'
          }
        }

        stage('Setup') {
          steps {
            sh 'pip install --no-cache-dir --upgrade pip'
            sh 'pip install --no-cache-dir -r scripts/requirements.txt'
            sh 'ln -s src/__main__.py abricot'
            sh 'chmod +x abricot'
            sh 'rm -rf abricot-tests/'
            sh 'git clone https://github.com/socialeonet/Abricot-Tests.git abricot-tests'
          }
        }

      }
    }

    stage('Tests') {
      environment {
        JENKINS = 'true'
      }
      parallel {
        stage('G1: Bad file Header') {
          steps {
            sh '''cd abricot-tests/G1/C
${WORKSPACE}/abricot --status'''
            sh '''cd abricot-tests/G1/H
${WORKSPACE}/abricot --status'''
          }
        }

        stage('G2: There should be only one line between each fonction') {
          steps {
            sh '''cd abricot-tests/G2/1
${WORKSPACE}/abricot --status'''
            sh '''cd abricot-tests/G2/2
${WORKSPACE}/abricot --status'''
          }
        }

        stage('G3: Preprocessor directive must be indented') {
          steps {
            sh '''cd abricot-tests/G3
${WORKSPACE}/abricot --status'''
          }
        }

        stage('G4: Global Variable must be const') {
          steps {
            sh '''cd abricot-tests/G4
${WORKSPACE}/abricot --status'''
          }
        }

        stage('G6: #include should only contain .h files') {
          steps {
            sh '''cd abricot-tests/G6
${WORKSPACE}/abricot --status'''
          }
        }

        stage('G7: Line should finish only end with a backslash n') {
          steps {
            sh '''cd abricot-tests/G7
${WORKSPACE}/abricot --status'''
          }
        }

        stage('G8: Trailing space') {
          steps {
            sh '''cd abricot-tests/G8
${WORKSPACE}/abricot --status'''
          }
        }

        stage('G9: Leading/Trailing lines') {
          steps {
            sh '''cd abricot-tests/G9
${WORKSPACE}/abricot --all --status'''
          }
        }

        stage('C1: There should not be more than 3 depth (conditionnal branching)') {
          steps {
            sh '''cd abricot-tests/C1
${WORKSPACE}/abricot --status'''
          }
        }

        stage('A3: Missing Line Break') {
          steps {
            sh '''cd abricot-tests/A3
${WORKSPACE}/abricot --status'''
          }
        }

        stage('L1: Code line content') {
          steps {
            sh '''cd abricot-tests/L1/1
${WORKSPACE}/abricot --all --status'''
            sh '''cd abricot-tests/L1/2
${WORKSPACE}/abricot --all --status'''
            sh '''cd abricot-tests/L1/3
${WORKSPACE}/abricot --all --status'''
            sh '''cd abricot-tests/L1/4
${WORKSPACE}/abricot --all --status'''
            sh '''cd abricot-tests/L1/5
${WORKSPACE}/abricot --all --status'''
          }
        }

        stage('L2: Bad indentation') {
          steps {
            sh '''cd abricot-tests/L2
${WORKSPACE}/abricot --status'''
          }
        }

        stage('L3: Misplaced spaces') {
          steps {
            sh '''cd abricot-tests/L3
${WORKSPACE}/abricot --status'''
          }
        }

        stage('L4: Misplaced curly bracket') {
          steps {
            sh '''cd abricot-tests/L4
${WORKSPACE}/abricot --status'''
          }
        }

        stage('L5: Variable declaration') {
          steps {
            sh '''cd abricot-tests/L5/1
${WORKSPACE}/abricot --all --status'''
            sh '''cd abricot-tests/L5/2
${WORKSPACE}/abricot --all --status'''
          }
        }

        stage('L6: Line jumps') {
          steps {
            sh '''cd abricot-tests/L6
${WORKSPACE}/abricot --all --status'''
          }
        }

        stage('O1: Check useless file') {
          steps {
            sh '''cd abricot-tests/O1/
cd "#"
${WORKSPACE}/abricot --status'''
            sh '''cd abricot-tests/O1/
cd "~"
${WORKSPACE}/abricot --status'''
            sh '''cd abricot-tests/O1/D
${WORKSPACE}/abricot --status'''
            sh '''cd abricot-tests/O1/A
${WORKSPACE}/abricot --status'''
            sh '''cd abricot-tests/O1/GCH
${WORKSPACE}/abricot --status'''
            sh '''cd abricot-tests/O1/O
${WORKSPACE}/abricot --status'''
            sh '''cd abricot-tests/O1/SO
${WORKSPACE}/abricot --status'''
          }
        }

        stage('O3: Too many functions in a file') {
          steps {
            sh '''cd abricot-tests/O3
${WORKSPACE}/abricot --status'''
          }
        }

        stage('O4: Snake case convention') {
          steps {
            sh '''cd abricot-tests/O4
${WORKSPACE}/abricot --status'''
          }
        }

        stage('F5: More than 4 arguments in a function') {
          steps {
            sh '''cd abricot-tests/F5/more
${WORKSPACE}/abricot --status'''
          }
        }

        stage('F5: Argumentless function') {
          steps {
            sh '''cd abricot-tests/F5/argumentless
${WORKSPACE}/abricot --status'''
          }
        }

        stage('F6: Comments inside of function') {
          steps {
            sh '''cd abricot-tests/F6
${WORKSPACE}/abricot --status'''
          }
        }

        stage('H2: Header not protected from doucle inclusion') {
          steps {
            sh '''cd abricot-tests/H2/1
${WORKSPACE}/abricot --status'''
            sh '''cd abricot-tests/H2/2
${WORKSPACE}/abricot --status'''
          }
        }

        stage('V1: Naming identifiers') {
          steps {
            sh '''cd abricot-tests/V1/1
${WORKSPACE}/abricot --all --status'''
            sh '''cd abricot-tests/V1/2
${WORKSPACE}/abricot --all --status'''
            sh '''cd abricot-tests/V1/3
${WORKSPACE}/abricot --all --status'''
            sh '''cd abricot-tests/V1/4
${WORKSPACE}/abricot --all --status'''
          }
        }

        stage('V3: Pointers') {
          steps {
            sh '''cd abricot-tests/V3/1
${WORKSPACE}/abricot --all --status'''
            sh '''cd abricot-tests/V3/2
${WORKSPACE}/abricot --all --status'''
          }
        }
      }
    }
  }
}
