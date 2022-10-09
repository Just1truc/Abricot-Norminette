import os

def getSourceFileNames() -> List[str]:
    res = []
    # recursiveley get all files in the current directory
    for root, dirs, files in os.walk(os.path.dirname(__file__)):
        for file in files:
            res.append(os.path.join(root, file))
    return res