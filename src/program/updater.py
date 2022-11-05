import os
import requests
from program.print import printc, Colors
from __init__ import __version__

URL_BASE = "https://raw.githubusercontent.com/Just1truc/Abricot-Norminette"
VERSION_FILE = "%s/VERSION" % URL_BASE
UPDATE_FILE = "%s/get_abricot.sh" % URL_BASE


def getLatestVersion():
    try:
        return requests.get(VERSION_FILE).text
    except:
        printc("Unable to get the current version of Abricot, check your internet connection...", color=Colors.RED)
        exit()


def update():
    latestVersion = getLatestVersion()
    if (latestVersion == __version__):
        printc("Abricot is already up to date!", color=Colors.GREEN)
        exit()
    print("Updating Abricot...")
    os.system("curl %s | sh" % UPDATE_FILE)
    exit()
