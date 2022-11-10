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


# if clang-format or pip is not installed
if ! [ -x "$(command -v clang-format)" || -x "$(command -v pip)" ]; then
    if ! [ "$(uname)" == "Darwin" ]; then
        tput sgr 0
        echo "=> Installing clang-format..."
        if [ -x "$(command -v dnf)" ]; then
            sudo dnf install clang-tools-extra pip || (tput setaf 1; echo "=> Error: clang-tools-extra install went wrong"; tput sgr0; exit 1)
        elif [ -x "$(command -v apt-get)" ]; then
            sudo apt-get install clang-format pip || (tput setaf 1; echo "=> Error: clang-format install went wrong"; tput sgr0; exit 1)
        elif [ -x "$(command -v zypper)" ]; then
            sudo zypper install clang-format python3-pip || (tput setaf 1; echo "=> Error: clang-format install went wrong"; tput sgr0; exit 1)
        elif [ -x "$(command -v pacman)" ]; then
            sudo pacman -S clang python-pip || (tput setaf 1; echo "=> Error: clang-format install went wrong"; tput sgr0; exit 1)
        else
            tput setaf 1
            echo "=> Error: Your distribution is not supported"
            tput sgr0
            exit 1
        fi
        echo "=> Installation of clang done"
    else if [ "$(uname -s)" == "Darwin" ]; then
        if ! [ -x "$(command -v brew)" ]; then
            tput sgr 0
            echo "=> Brew is not installed"
            echo "=> Installing brew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
            tput setaf 2
            echo "=> Brew installed"
            tput sgr0
        fi
        tput setaf 0
        echo "=> Installing clang-format..."
        brew install clang-format
        tput setaf 2
        echo "=> Installation of clang done"
        tput sgr0
    fi
fi
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
