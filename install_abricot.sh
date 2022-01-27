#!/bin/sh
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
tput setaf 2
echo "=> Done copying source code"
tput sgr 0
echo "=> Erasing zsh alias if needed..."
OUTPUT=$(sudo cat ~/.zshrc | grep "alias abricot")
if [[ $OUTPUT != "" ]]
then
    word="alias abricot='sh ~/.Abricot-script/brico.sh'"
    vide=""
    sed 's/$word/$vide/g' ~/.zshrc > ~/.zshrc
    tput setaf 2
    echo "=> Alias erased"
    tput sgr 0
fi
echo "=> Copying source code into bin..."
sudo cp abricot /usr/local/bin
tput setaf 2
echo "=> Done copying"
tput sgr0
tput setaf 2
echo "=> Installation Done"
tput sgr 0
echo "=> Restarting zsh"
zsh
