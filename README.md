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
- **G9** Trailing lines

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

- **F3** A line lenght shoud not exceed 80 columns
- **F4** A function should not exceed 20 lines
- **F5** More than 4 arguments in a function or argumentless function
- **F6** Comments inside of functions

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
| Debian based 	| ✅             	|
| Fedora based 	| ✅             	|
| macOS        	| ✅             	|
| Windows      	| ⚠️ WSL advised 	|


## Credits

#### Programation : Justin Duc

[![linkeding bage](https://img.shields.io/badge/-linkedin-0A66C2?logo=linkedin&style=for-the-badge)](https://www.linkedin.com/in/justin-duc-51b09b225/)
[![git hub bage](https://img.shields.io/badge/-GitHub-181717?logo=GitHub&style=for-the-badge)](https://github.com/Just1truc)
[![mail](https://img.shields.io/badge/-Mail-0078D4?logo=Microsoft-Outlook&style=for-the-badge)](mailto:justin.duc@epitech.eu)

#### Redaction : Baptiste Leroyer

[![linkeding bage](https://img.shields.io/badge/-linkedin-0A66C2?logo=linkedin&style=for-the-badge)](https://www.linkedin.com/in/baptiste-leroyer-a69894227/)
[![git hub bage](https://img.shields.io/badge/-GitHub-181717?logo=GitHub&style=for-the-badge)](https://github.com/ZiplEix)
[![mail](https://img.shields.io/badge/-Mail-0078D4?logo=Microsoft-Outlook&style=for-the-badge)](mailto:baptiste.leroyer@epitech.eu)

#### L3 handling : Mathias André

[![linkeding bage](https://img.shields.io/badge/-linkedin-0A66C2?logo=linkedin&style=for-the-badge)](https://www.linkedin.com/in/mathias-andr%C3%A9-a7b30721a/)
[![git hub bage](https://img.shields.io/badge/-GitHub-181717?logo=GitHub&style=for-the-badge)](https://github.com/MathiDEV)
[![mail](https://img.shields.io/badge/-Mail-0078D4?logo=Microsoft-Outlook&style=for-the-badge)](mailto:mathias.andre@epitech.eu)

#### Quality: Thomas Mazaud

[![linkeding bage](https://img.shields.io/badge/-linkedin-0A66C2?logo=linkedin&style=for-the-badge)](https://www.linkedin.com/in/thomasmazaud/)
[![git hub bage](https://img.shields.io/badge/-GitHub-181717?logo=GitHub&style=for-the-badge)](https://github.com/Fyroeo)
[![mail](https://img.shields.io/badge/-Mail-0078D4?logo=Microsoft-Outlook&style=for-the-badge)](mailto:thomas.mazaud@epitech.eu)
