def isBinary(file: str) -> bool:
    try:
        with open(file, 'tr') as check_file:
            check_file.read()
            return False
    except UnicodeDecodeError:
        return True
    except:
        return False