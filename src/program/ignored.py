import os

from program.print import Colors, printc

def getIgnoredFiles():
    try:
        res = os.system("git check-ignore $(find . -type f -print) > .abricotignore 2> /dev/null")
        if res != 0:
            printc("ERROR: This directory is not a git repository...", bold=True, color=Colors.RED)
            os.system("rm .abricotignore")
            raise FileNotFoundError()
        with open(".abricotignore", "r") as f:
            ignored = f.readlines()
        os.system("rm .abricotignore")
        return [x[2:].replace("\n", "") if x.startswith("./") else x.replace("\n", "") for x in ignored]
    except FileNotFoundError:
        exit(1)
    except:
        return []
    