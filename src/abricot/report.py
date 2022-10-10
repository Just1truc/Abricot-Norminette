all_errors = {}

def report(file: str, line: int, code: str) -> None:
    if code not in all_errors:
        all_errors[code] = []
    all_errors[code].append((file, line))

def getAllErrors() -> dict[str, list[tuple[str, int]]]:
    return all_errors

