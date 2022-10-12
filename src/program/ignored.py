import os

def getIgnoredFiles():
    try:
        os.system("git check-ignore $(find . -type f -print) > .abricotignore")
        with open(".abricotignore", "r") as f:
            ignored = f.readlines()
        os.system("rm .abricotignore")
        return [x[2:].replace("\n", "") if x.startswith("./") else x.replace("\n", "") for x in ignored]
    except:
        return []
    