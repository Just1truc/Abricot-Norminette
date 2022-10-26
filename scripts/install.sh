#!/bin/bash

tput setaf 3
tput bold
echo "     _    _          _           _   
    / \  | |__  _ __(_) ___ ___ | |_ 
   / _ \ | '_ \| '__| |/ __/ _ \| __|
  / ___ \| |_) | |  | | (_| (_) | |_ 
 /_/   \_\_.__/|_|  |_|\___\___/ \__|
                                  "
tput sgr0

echo "=> Erasing old version"
sudo rm -rf ~/.Abricot-script/
sudo rm -rf /usr/local/lib/Abricot_scripts
sudo rm -rf /usr/local/lib/Abricot_update
sudo rm -rf /usr/local/lib/abricot
sudo rm -rf /usr/local/bin/abricot
tput setaf 2
echo "=> Done erasing"
tput sgr0


# if clang-format is not installed
if ! [ -x "$(command -v clang-format)" ]; then
    tput sgr 0
    echo "=> Installing clang-format..."
    sudo dnf -y install clang-tools-extra 2> /dev/null
    sudo apt update; sudo apt -y install clang-format 2> /dev/null
    sudo zypper -y install clang-tools-extra 2> /dev/null
    tput setaf 2
    echo "=> Installation of clang done"
else
    tput setaf 2
    echo "=> clang-format found"
fi
BASEDIR=$(dirname "$0")

tput sgr 0
echo "=> Installing checker rules..."
python3 "$BASEDIR/fruitmixer.py"
tput setaf 2

tput sgr 0
echo "=> Installing python dependencies..."
pip install -r "$BASEDIR/requirements.txt" 2>&1 > /dev/null
tput setaf 2
echo "=> Installation of requirements done"

tput init
echo "=> Copying source code..."
sudo mkdir /usr/local/lib/abricot
sudo cp -R "$BASEDIR/../src/." /usr/local/lib/abricot
tput setaf 2
echo "=> Done copying"
tput sgr0

echo "=> Copying source code into bin..."
sudo chmod 755 /usr/local/lib/abricot/__main__.py
sudo ln -s /usr/local/lib/abricot/__main__.py /usr/local/bin/abricot
tput setaf 2
echo "=> Done copying"
tput sgr0
tput setaf 2
echo "=> Installation Done"
tput sgr 0
