# Abricot moulinette

Welcome to Abricot Norminette, a checker for C project files that check the coding style errors for EPITECH


## Files checked
- *.c
- *.h
- *Makefile

## Error handling

G 6, 1, 2, 3, 8 :

- include folder should not contain .h files;
- bad file header; 
- there should be only one line between each fonction; 
- preprocessor directive must be indented; 
- trailing space; 

C 1

- there should not be more than 3 depth

L 2, 3, 4

- bad indentation; 
- misplaced spaces; 
- misplaced curly bracket; 

O 1, 4, 3

- check useless file; 
- snake case convention; 
- to many fonctions in a file; *

F 3, 4, 

- a line lenght shoud not exceed 80 columns; 
- a fonction should not exceed 20 lines; 
- more than 4 arguments in a fonction; 

## Installation

Clone the repository in your home folder :
```
git clone https://github.com/Just1truc/Abricot-Norminette.git ~/Abricot-Norminette
```
Get into the repository folder and execute the "install_abricot.sh" file :
```
cd ~/Abricot-Norminette && ./install_abricot.sh
```

## Update instrutions

Updates are regulary made.<br />
To update Abricot, please use the following command :
```
abricot --update
```

## Compatibility

Python3+ should be installed on your computer for Abricot to work.

| OS           	| Compatible ?  	|
|--------------	|---------------	|
| Debian based 	| ✅             	|
| Fedora based 	| ✅             	|
| macOS        	| ✅             	|
| Windows      	| ⚠️ WSL advised 	|


## Credits

Programation : Justin Duc;

Redaction : Baptiste Leroyer;

L3 handling : Mathias André;

Quality: Thomas Mazaud
