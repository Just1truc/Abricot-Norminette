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
            Assert('G1/C/ERROR', 1)
            Assert('G1/C/OK', 0)
            Assert('G1/H/ERROR', 1)
            Assert('G1/H/OK', 0)
          }
        }
        stage('G2: There should be only one line between each fonction') {
          steps {
            Assert('G2/2_separated_lines/ERROR', 1)
            Assert('G2/2_separated_lines/OK', 0)
            Assert('G2/no_separeted_line/ERROR', 1)
            Assert('G2/no_separeted_line/OK', 0)
          }
        }
        stage('G3: Preprocessor directive must be indented') {
          steps {
            Assert('G3/ERROR', 1)
            Assert('G3/OK', 0)
          }
        }
        stage('G4: Global Variable must be const') {
          steps {
            Assert('G4/ERROR', 1)
            Assert('G4/OK', 0)
          }
        }
        stage('G5: #include should only contain .h files') {
          steps {
            Assert('G5/ERROR', 1)
            Assert('G5/OK', 0)
          }
        }
        stage('G8: Global variable must be const') {
          steps {
            Assert('G7/ERROR', 1)
            Assert('G7/OK', 0)
          }
        }
        stage('G7: Trailing space') {
          steps {
            Assert('G7/ERROR', 1)
            Assert('G7/OK', 0)
          }
        }
        stage('C1: There should not be more than 3 depth (conditionnal branching)') {
          steps {
            Assert('C1/ERROR', 1)
            Assert('C1/OK', 0)
          }
        }
        stage('C3: GOTO is forbidden') {
          steps {
            Assert('C3/ERROR', 1)
            Assert('C3/OK', 0)
          }
        }
        stage('A3: Missing Line Break') {
          steps {
            Assert('A3/ERROR', 1)
            Assert('A3/OK', 0)
          }
        }
        stage('L1: Code line content') {
          steps {
            Assert('L1/1/ERROR', 1)
            Assert('L1/1/OK', 0)
            Assert('L1/2/ERROR', 1)
            Assert('L1/2/OK', 0)
            Assert('L1/3/ERROR', 1)
            Assert('L1/3/OK', 0)
            Assert('L1/4/ERROR', 1)
            Assert('L1/4/OK', 0)
            Assert('L1/5/ERROR', 1)
            Assert('L1/5/OK', 0)
          }
        }
        stage('L2: Bad indentation') {
          steps {
            Assert('L2/ERROR', 1)
            Assert('L2/OK', 0)
          }
        }
        stage('L3: Misplaced spaces') {
          steps {
            Assert('L3/ERROR', 1)
            Assert('L3/OK', 0)
          }
        }
        stage('L4: Misplaced curly bracket') {
          steps {
            Assert('L4/ERROR', 1)
            Assert('L4/OK', 0)
          }
        }
        stage('L5: Variable declaration') {
          steps {
            Assert('L5/1/ERROR', 1)
            Assert('L5/1/OK', 0)
            Assert('L5/2/ERROR', 1)
            Assert('L5/2/OK', 0)
          }
        }
        stage('L6: Line jumps') {
          steps {
            Assert('L6/ERROR', 1)
            Assert('L6/OK', 0)
          }
        }
        stage('O1: Check useless file') {
          steps {
            Assert('O1/#/ERROR', 1)
            Assert('O1/#/OK', 0)
            Assert('O1/~/ERROR', 1)
            Assert('O1/~/OK', 0)
            Assert('O1/D/ERROR', 1)
            Assert('O1/D/OK', 0)
            Assert('O1/A/ERROR', 1)
            Assert('O1/A/OK', 0)
            Assert('O1/GCH/ERROR', 1)
            Assert('O1/GCH/OK', 0)
            Assert('O1/O/ERROR', 1)
            Assert('O1/O/OK', 0)
            Assert('O1/SO/ERROR', 1)
            Assert('O1/SO/OK', 0)
          }
        }
        stage('O3: Too many functions in a file') {
          steps {
            Assert('O3/ERROR', 1)
            Assert('O3/OK', 0)
          }
        }
        stage('O4: Snake case convention') {
          steps {
            Assert('O4/ERROR', 1)
            Assert('O4/OK', 0)
          }
        }
        stage('F3: Too long line') {
          steps {
            Assert('F3/more/ERROR', 1)
            Assert('F3/more/OK', 0)
          }
        }
        stage('F4: Too long function') {
          steps {
            Assert('F4/ERROR', 1)
            Assert('F4/OK', 0)
          }
        }
        stage('F5: More than 4 arguments in a function') {
          steps {
            Assert('F5/ERROR', 1)
            Assert('F5/OK', 0)
          }
        }
        stage('F6: Argumentless function') {
          steps {
            Assert('F6/ERROR', 1)
            Assert('F6/OK', 0)
          }
        }
        stage('H2: Header not protected from doucle inclusion') {
          steps {
            Assert('H2/1/ERROR', 1)
            Assert('H2/1/OK', 0)
            Assert('H2/2/ERROR', 1)
            Assert('H2/2/OK', 0)
          }
        }
        stage('V1: Naming identifiers') {
          steps {
            Assert('V1/1/ERROR', 1)
            Assert('V1/1/OK', 0)
            Assert('V1/2/ERROR', 1)
            Assert('V1/2/OK', 0)
            Assert('V1/3/ERROR', 1)
            Assert('V1/3/OK', 0)
            Assert('V1/4/ERROR', 1)
            Assert('V1/4/OK', 0)
          }
        }
        stage('V3: Pointers') {
          steps {
            Assert('V3/1/ERROR', 1)
            Assert('V3/1/OK', 0)
            Assert('V3/2/ERROR', 1)
            Assert('V3/2/OK', 0)
          }
        }
      }
    }
  }
}