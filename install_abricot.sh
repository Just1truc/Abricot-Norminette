#!/bin/bash
echo "=> Erasing old version"
FILE=~/.Abricot-script/
if [ -d $FILE ]
then
    sudo rm -rf ~/.Abricot-script/
fi
tput setaf 2
FILE=/usr/local/lib/Abricot_scripts
if [ -d $FILE ]
then
    sudo rm -rf /usr/local/lib/Abricot_scripts
fi
echo "=> Erasing Done"
tput sgr 0
echo "=> Installing clang-format..."
sudo dnf -y install clang-tools-extra 2> /dev/null
sudo apt-get -y install clang-tools-extra 2> /dev/null
sudo zypper -y install clang-tools-extra 2> /dev/null
tput setaf 2
echo "=> Installation of clang done"
tput init
echo "=> Copying source code..."
sudo mkdir /usr/local/lib/Abricot_scripts
sudo cp -R . /usr/local/lib/Abricot_scripts
FILE=/usr/local/lib/Abricot_update
if [ -d $FILE ]
then
    echo "=> Updating"
else
    sudo mkdir /usr/local/lib/Abricot_update
    sudo cp -R . /usr/local/lib/Abricot_update
    sudo chmod -R 777 /usr/local/lib/Abricot_update
fi
sudo chmod -R 777 /usr/local/lib/Abricot_scripts
tput setaf 2
echo "=> Done copying source code"
tput sgr 0
echo "=> Erasing zsh alias if needed..."
FILE=~/.zshrc
if [ -d $FILE ]
then
    OUTPUT=$(sudo cat ~/.zshrc | grep "alias abricot")
    if [[ $OUTPUT != "" ]]
    then
        TEST=$(sudo cat ~/.zshrc | grep "unalias abricot")
        if [[ $TEST == "" ]]
        then
            echo "unalias abricot" >> ~/.zshrc
        fi
    fi
fi
echo "=> Copying source code into bin..."
sudo cp abricot /usr/local/bin
tput setaf 2
echo "=> Done copying"
tput sgr0
tput setaf 2
echo "=> Installation Done"
tput sgr 0
