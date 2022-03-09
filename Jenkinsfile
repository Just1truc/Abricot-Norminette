pipeline {
  agent any
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
            sh 'chmod +x abricot'
          }
        }

      }
    }

    stage('Tests') {
      environment {
        JENKINS = 'true'
      }
      parallel {
        stage('G1: Bad file Header (C File)') {
          steps {
            sh '''cd ~/abricot-tests/G1/C
${WORKSPACE}/abricot'''
          }
        }

        stage('G1: Bad file Header (H File)') {
          steps {
            sh '''cd ~/abricot-tests/G1/H
${WORKSPACE}/abricot'''
          }
        }

        stage('G2: There should be only one line between each fonction') {
          steps {
            sh '''cd ~/abricot-tests/G2
${WORKSPACE}/abricot'''
          }
        }

        stage('G3: Preprocessor directive must be indented') {
          steps {
            sh '''cd ~/abricot-tests/G3
${WORKSPACE}/abricot'''
          }
        }

        stage('G4: Global Variable must be const') {
          steps {
            sh '''cd ~/abricot-tests/G4
${WORKSPACE}/abricot'''
          }
        }

        stage('G6: #include should only contain .h files') {
          steps {
            sh '''cd ~/abricot-tests/G6
${WORKSPACE}/abricot'''
          }
        }

        stage('G7: Line should finish only end with a backslash n') {
          steps {
            sh '''cd ~/abricot-tests/G7
${WORKSPACE}/abricot'''
          }
        }

        stage('G8: Trailing space') {
          steps {
            sh '''cd ~/abricot-tests/G8
${WORKSPACE}/abricot'''
          }
        }

        stage('C1: There should not be more than 3 depth (conditionnal branching)') {
          steps {
            sh '''cd ~/abricot-tests/C1
${WORKSPACE}/abricot'''
          }
        }

        stage('A3: Missing Line Break') {
          steps {
            sh '''cd ~/abricot-tests/A3
${WORKSPACE}/abricot'''
          }
        }

        stage('L2: Bad indentation') {
          steps {
            sh '''cd ~/abricot-tests/L2
${WORKSPACE}/abricot'''
          }
        }

        stage('L3: Misplaced spaces') {
          steps {
            sh '''cd ~/abricot-tests/L3
${WORKSPACE}/abricot'''
          }
        }

        stage('L4: Misplaced curly bracket') {
          steps {
            sh '''cd ~/abricot-tests/L4
${WORKSPACE}/abricot'''
          }
        }

        stage('O1: Check useless file (#)') {
          steps {
            sh '''cd ~/abricot-tests/O1/
cd "#"
${WORKSPACE}/abricot'''
          }
        }

        stage('O1: Check useless file (~)') {
          steps {
            sh '''cd ~/abricot-tests/O1/
cd "~"
${WORKSPACE}/abricot'''
          }
        }

        stage('O1: Check useless file (D)') {
          steps {
            sh '''cd ~/abricot-tests/O1/D
${WORKSPACE}/abricot'''
          }
        }

        stage('O1: Check useless file (A)') {
          steps {
            sh '''cd ~/abricot-tests/O1/A
${WORKSPACE}/abricot'''
          }
        }

        stage('O1: Check useless file (GCH)') {
          steps {
            sh '''cd ~/abricot-tests/O1/GCH
${WORKSPACE}/abricot'''
          }
        }

        stage('O1: Check useless file (O)') {
          steps {
            sh '''cd ~/abricot-tests/O1/O
${WORKSPACE}/abricot'''
          }
        }

        stage('O1: Check useless file (SO)') {
          steps {
            sh '''cd ~/abricot-tests/O1/SO
${WORKSPACE}/abricot'''
          }
        }

        stage('O3: Too many fonctions in a file') {
          steps {
            sh '''cd ~/abricot-tests/O3
${WORKSPACE}/abricot'''
          }
        }

        stage('O4: Snake case convention') {
          steps {
            sh '''cd ~/abricot-tests/O4
${WORKSPACE}/abricot'''
          }
        }

        stage('F5: More than 4 arguments in a function') {
          steps {
            sh '''cd ~/abricot-tests/F5/more
${WORKSPACE}/abricot'''
          }
        }

        stage('F5: Argumentless function') {
          steps {
            sh '''cd ~/abricot-tests/F5/argumentless
${WORKSPACE}/abricot'''
          }
        }

      }
    }

  }
}