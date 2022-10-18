def Assert(dir, status) {
  res = sh(
    script: "${WORKSPACE}/abricot abricot-tests/${dir} --status --format=plain",
    returnStatus: true
  )
  if (res != status) {
    error "${dir}: expected ${status}, got ${res}"
  }
}

pipeline {
  agent {
    dockerfile true
  }
  environment {
    JENKINS = 'true'
    PYTHONPATH = '/home/jenkins-agent/workspace/Abricot-Norminette_develop/modules'
  }
  stages {
    stage('Env. info') {
      parallel {
        stage('Env. info') {
          steps {
            sh 'python -V'
            sh 'python -c "import sys; print(sys.path)"'
          }
        }
        stage('Setup') {
          steps {
            sh 'ln -s src/__main__.py abricot'
            sh 'chmod +x abricot'
            sh 'pip3 install --target=${WORKSPACE}/modules -r scripts/requirements.txt'
            sh 'rm -rf abricot-tests/'
            sh 'git clone https://github.com/socialeonet/Abricot-Tests.git abricot-tests'
          }
        }
      }
    }
    stage('Tests') {
      parallel {
        stage('G1: Bad file Header') {
          steps {
            Assert('G1/C', 1)
            Assert('G1/H', 1)
          }
        }
        stage('G2: There should be only one line between each fonction') {
          steps {
            Assert('G2/1', 1)
            Assert('G2/2', 1)
          }
        }
        stage('G3: Preprocessor directive must be indented') {
          steps {
            Assert('G3', 1)
          }
        }
        stage('G4: Global Variable must be const') {
          steps {
            Assert('G4', 1)
          }
        }
        stage('G6: #include should only contain .h files') {
          steps {
            Assert('G6', 1)
          }
        }
        stage('G7: Line should finish only end with a backslash n') {
          steps {
            Assert('G7', 1)
          }
        }
        stage('G8: Trailing space') {
          steps {
            Assert('G8', 1)
          }
        }
        stage('G9: Leading/Trailing lines') {
          steps {
            Assert('G9', 1)
          }
        }
        stage('C1: There should not be more than 3 depth (conditionnal branching)') {
          steps {
            Assert('C1', 1)
          }
        }
        stage('A3: Missing Line Break') {
          steps {
            Assert('A3', 1)
          }
        }
        stage('L1: Code line content') {
          steps {
            Assert('L1/1', 1)
            Assert('L1/2', 1)
            Assert('L1/3', 1)
            Assert('L1/4', 1)
            Assert('L1/5', 1)
          }
        }
        stage('L2: Bad indentation') {
          steps {
            Assert('L2', 1)
          }
        }
        stage('L3: Misplaced spaces') {
          steps {
            Assert('L3', 1)
          }
        }
        stage('L4: Misplaced curly bracket') {
          steps {
            Assert('L4', 1)
          }
        }
        stage('L5: Variable declaration') {
          steps {
            Assert('L5/1', 1)
            Assert('L5/2', 1)
          }
        }
        stage('L6: Line jumps') {
          steps {
            Assert('L6', 1)
          }
        }
        stage('O1: Check useless file') {
          steps {
            Assert('O1/#', 1)
            Assert('O1/~', 1)
            Assert('O1/D', 1)
            Assert('O1/A', 1)
            Assert('O1/GCH', 1)
            Assert('O1/O', 1)
            Assert('O1/SO', 1)
          }
        }
        stage('O3: Too many functions in a file') {
          steps {
            Assert('O3', 1)
          }
        }
        stage('O4: Snake case convention') {
          steps {
            Assert('O4', 1)
          }
        }
        stage('F5: More than 4 arguments in a function') {
          steps {
            Assert('F5/more', 1)
          }
        }
        stage('F5: Argumentless function') {
          steps {
            Assert('F5/argumentless', 1)
          }
        }
        stage('F6: Comments inside of function') {
          steps {
            Assert('F6', 1)
          }
        }
        stage('H2: Header not protected from doucle inclusion') {
          steps {
            Assert('H2/1', 1)
            Assert('H2/2', 1)
          }
        }
        stage('V1: Naming identifiers') {
          steps {
            Assert('V1/1', 1)
            Assert('V1/2', 1)
            Assert('V1/3', 1)
            Assert('V1/4', 1)
          }
        }
        stage('V3: Pointers') {
          steps {
            Assert('V3/1', 1)
            Assert('V3/2', 1)
          }
        }
      }
    }
  }
}