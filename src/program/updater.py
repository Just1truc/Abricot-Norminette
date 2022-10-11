import requests
from program.print import printc, Colors
from __init__ import __version__

VERSION_FILE = "https://raw.githubusercontent.com/Just1truc/Abricot-Norminette/develop/VERSION"

def getCurrentVersion():
    try:
        return requests.get(VERSION_FILE).text
    except:
        printc("Unable to get the current version of Abricot, check your internet connection...", color=Colors.RED)
        exit()

def update():
    currentVersion = getCurrentVersion()
    if (currentVersion == __version__):
        printc("Abricot is already up to date!", color=Colors.GREEN)
        exit()
    print("Updating Abricot...")
    exit()