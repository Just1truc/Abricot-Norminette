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
${WORKSPACE}/abricot '''
          }
        }

        stage('G1: Bad file Header (H File)') {
          steps {
            sh '''cd ~/abricot-tests/G1/H
${WORKSPACE}/abricot'''
          }
        }

      }
    }

  }
}