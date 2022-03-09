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

      }
    }

  }
}