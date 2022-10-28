savedLines = {}

def getAllLines(file: str):
    if file in savedLines:
        return savedLines[file]

def prepareGetAllLines(files):
    for file in files:
         with open(file, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            lines = map(lambda x: x[:-1] if x.endswith('\n') else x, lines)
            savedLines[file] = list(lines)
