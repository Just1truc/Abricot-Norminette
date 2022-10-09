def getAllLines(file: str) -> bool:
    with open(file, 'r') as f:
        return f.readlines()