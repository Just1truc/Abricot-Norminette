import os

def getSourceFileNames() -> list[str]:
    res = []
    # recursiveley get all files in the current directory
    for root, dirs, files in os.walk('.'):
        for file in files:
            res.append(os.path.join(root, file))
    return res