#!/bin/sh
echo "=> Erasing old version"
FILE=~/.Abricot-script/
if [ -d $FILE ]
then
    sudo rm -rf ~/.Abricot-script/
fi
tput setaf 2
echo "=> Erasing Done"
tput sgr 0
echo "=> Installing clang-format..."
sudo pacman -S clang-tools-extra &> /dev/null
sudo dnf install clang-tools-extra &> /dev/null
sudo apt-get install clang-tools-extra &> /dev/null
sudo zypper install clang-tools-extra &> /dev/null
tput setaf 2
echo "=> Installation of clang done"
tput init
echo "=> Adding necessary file to a proper functionning..."
mkdir ~/.Abricot-script
tput setaf 2
echo "=> Done adding"
tput sgr 0
echo "=> Copying source code..."
cp -R . ~/.Abricot-script/
tput setaf 2
echo "=> Done copying source code"
tput sgr 0
echo "=> Adding zsh alias if needed..."
OUTPUT=$(sudo cat ~/.zshrc | grep "alias abricot")
if [[ $OUTPUT == "" ]]
then
    echo "alias abricot='sh ~/.Abricot-script/brico.sh'" >> ~/.zshrc
    tput setaf 2
    echo "=> Alias added"
    tput sgr 0
fi
tput setaf 2
echo "=> Installation Done"
tput sgr 0
echo "=> Restarting zsh"
zsh
