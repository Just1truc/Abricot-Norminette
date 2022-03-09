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

        stage('G7: Line should finish only end with a "\n"') {
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

      }
    }

  }
}