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
            sh 'alias abricot=\'`pwd`/abricot\''
          }
        }

      }
    }

    stage('G1: Bad file Header (C File)') {
      environment {
        JENKINS = ''
      }
      parallel {
        stage('G1: Bad file Header (C File)') {
          steps {
            sh '''cd ~/abricot-tests/G1/C
abricot'''
          }
        }

        stage('G1: Bad file Header (H File)') {
          steps {
            sh '''cd ~/abricot-tests/G1/H
abricot'''
          }
        }

      }
    }

  }
}