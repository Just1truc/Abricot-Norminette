from abricot import getAllLines

def getLine(file: str, line: int) -> str:
    return getAllLines(file)[line - 1]
