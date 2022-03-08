pipeline {
  agent any
  stages {
    stage('Env. info') {
      steps {
        sh 'python -V'
      }
    }

    stage('G1: Bad file Header (C File)') {
      parallel {
        stage('G1: Bad file Header (C File)') {
          environment {
            JENKINS = 'true'
          }
          steps {
            writeFile(file: 'g1.c', text: '/* ** EPITECH PROJECT, 2021 ** B-CPE-110-LYN-1-1-pushswap-thomas.mazaud ** File description: ** File to create the doubly circular linked list */')
            sh 'abricot'
            sh 'rm g1.c'
          }
        }

        stage('G1: Bad file Header (H File)') {
          steps {
            writeFile(file: 'Makefile', text: '## ## EPITECH PROJECT, 2021 ## B-CPE-110-LYN-1-1-pushswap-thomas.mazaud ## File description: ## Makefile #')
            sh 'abricot'
            sh 'rm Makefile'
          }
        }

      }
    }

  }
}