# Abricot Norminette

Abricot Norminette is a file checker notifying the user of coding style errors.

## Files checked

- *.c
- *.h
- *Makefile
- Bad files

## Error handling

#### Global scope

- **G1** Bad file header
- **G2** There should be only one line between each fonction
- **G3** Preprocessor directive must be indented
- **G4** Global Variable must be const 
- **G6** #include should only contain .h files
- **G7** Line should finish only end with a "\n"
- **G8** Trailing space

####  Control structure

- **C1** There should not be more than 3 depth (conditionnal branching)
- **C3** Forbidden goto

####  Advanced

- **A3** Missing Line Break

#### Layout inside a function scope

- **L2** Bad indentation 
- **L3** Misplaced spaces
- **L4** Misplaced curly bracket

#### Files organization

- **O1** Check useless file
- **O3** Too many fonctions in a file
- **O4** Snake case convention

#### Functions

- **F3** A line lenght shoud not exceed 80 columns; 
- **F4** A fonction should not exceed 20 lines; 
- **F5** More than 4 arguments in a fonction or argumentless function; 

#### Header files

- **H2** Header not protected from doucle inclusion

## Installation

Clone the repository in your home folder :
```
git clone https://github.com/Just1truc/Abricot-Norminette.git ~/Abricot-Norminette
```
Get into the repository folder and execute the "install_abricot.sh" file :
```
cd ~/Abricot-Norminette && ./install_abricot.sh
```

## Updating

Updates are regulary made.<br />
To update Abricot, please use the following command :
```
abricot --update
```

## Compatibility

Python3+ should be installed on your computer for Abricot to work.

| OS           	| Compatible ?  	|
|--------------	|---------------	|
| Debian based 	|   ✅             	|
| Fedora based 	|   ✅             	|
| macOS        	|   ✅             	|
| Windows      	|   ⚠️ WSL advised 	|


## Credits

Programation : Justin Duc;

Redaction : Baptiste Leroyer;

L3 handling : Mathias André;

Quality: Thomas Mazaud
