def getAllLines(file: str) -> list[str]:
    with open(file, 'r') as f:
        content = f.read()
        lines = content.split('\n')
        lines = map(lambda x: x[:-1] if x.endswith('\n') else x, lines)
        return list(lines)
