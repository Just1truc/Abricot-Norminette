<p align="center">
    <img width=100 src=".github/assets/lebrico.png">
</p>

# Abricot Reborn

> During your projects you may be tempted to quickly and intuitively check your style mistakes thanks to a tool called **Automated Beautiful Recursive Integrated Coding Omissions Tracker**, better known as **Abricot**

**More seriously,** the Abricot development team has been thinking for some time about a more modern and more stable implementation of the norminette. This new year for Epitech is an opportunity to make it **compliant with current coding style rules.**

## Checked files

Here are the files affected by Abricot's style check:

<img height=16 src=".github/assets/files/cfile.png"> **C Source Files** _(*.c)_

<img height=16 src=".github/assets/files/hfile.png"> **C Header Files** _(*.h)_

<img height=16 src=".github/assets/files/makefile.png"> **Makefiles** 

_Abricot also looks for **unwanted files** in the repository..._

## Handled rules

#### Severities:
- <img height=16 src=".github/assets/severity/major.png"> **MAJOR**
- <img height=16 src=".github/assets/severity/minor.png"> **MINOR**
- <img height=16 src=".github/assets/severity/info.png"> **INFO**

#

#### Global scope

- <img height=16 src=".github/assets/severity/minor.png"> **C-G1** Bad file header
- <img height=16 src=".github/assets/severity/minor.png"> **C-G2** There should be only one line between each fonction
- <img height=16 src=".github/assets/severity/minor.png"> **C-G3** Preprocessor directive must be indented
- <img height=16 src=".github/assets/severity/major.png"> **C-G4** Global Variable must be const
- <img height=16 src=".github/assets/severity/minor.png"> **C-G6** #include should only contain .h files
- <img height=16 src=".github/assets/severity/minor.png"> **C-G7** Line should finish only end with a "\n"
- <img height=16 src=".github/assets/severity/minor.png"> **C-G8** Trailing space
- <img height=16 src=".github/assets/severity/minor.png"> **C-G9** Constant values

####  Control structure

- <img height=16 src=".github/assets/severity/major.png"> **C-C1** There should not be more than 3 depth (conditionnal branching)
- <img height=16 src=".github/assets/severity/major.png"> **C-C3** Forbidden goto

####  Advanced

- <img height=16 src=".github/assets/severity/info.png"> **C-A3** Missing Line Break

#### Layout inside a function scope

- <img height=16 src=".github/assets/severity/major.png"> **C-L1** Coding content
- <img height=16 src=".github/assets/severity/minor.png"> **C-L2** Bad indentation
- <img height=16 src=".github/assets/severity/minor.png"> **C-L3** Misplaced spaces
- <img height=16 src=".github/assets/severity/minor.png"> **C-L4** Misplaced curly bracket
- <img height=16 src=".github/assets/severity/major.png"> **C-L5** Bad variable declaration
- <img height=16 src=".github/assets/severity/minor.png"> **C-L6** Bad line break

#### Files organization

- <img height=16 src=".github/assets/severity/major.png"> **C-O1** Check useless file
- <img height=16 src=".github/assets/severity/major.png"> **C-O3** Too many fonctions in a file
- <img height=16 src=".github/assets/severity/major.png"> **C-O4** Snake case convention

#### Functions

- <img height=16 src=".github/assets/severity/major.png"> **C-F3** A line lenght shoud not exceed 80 columns
- <img height=16 src=".github/assets/severity/major.png"> **C-F4** A function should not exceed 20 lines
- <img height=16 src=".github/assets/severity/major.png"> **C-F5** More than 4 arguments in a function or argumentless function
- <img height=16 src=".github/assets/severity/major.png"> **C-F6** Comments inside of functions

#### Header files

- <img height=16 src=".github/assets/severity/major.png"> **H2** Header not protected from doucle inclusion

#### Variables and Types

- <img height=16 src=".github/assets/severity/minor.png"> **V1** Controlling structures and macros
- <img height=16 src=".github/assets/severity/minor.png"> **V3** Pointers position

## Installation



## Usage

We wanted to make Abricot usable at any time, without requesting superuser permissions and without creating intermediate files polluting your workspace.

You can launch a deep analysis with Abricot with the following simple command:

```bash
abricot
```

You can also take a look at all the additional features implemented with:

```bash
abricot -h
```

## Updating

Updates are regulary made.<br />
To keep Abricot up-to-date, please use the following command :
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

## Contribution [![Jenkins](https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins.dev.socialeo.eu%2Fjob%2FAbricot-Norminette%2Fjob%2Fmain%2F&label=Jenkins&logo=Jenkins&logoColor=red&style=for-the-badge)](https://jenkins.dev.socialeo.eu/job/Abricot-Norminette/)

Abricot is tested against every coding style errors using Jenkins on https://jenkins.dev.socialeo.eu/job/Abricot-Norminette/ <br />
After your contribution, you might want to check if the build is successful.

You might create a new branch before merging into the main branch so Jenkins will automatically test it within a minute.

## Credits

#### Lead Developper : Justin Duc

[![linkeding bage](https://img.shields.io/badge/-linkedin-0A66C2?logo=linkedin&style=for-the-badge)](https://www.linkedin.com/in/justin-duc-51b09b225/)
[![git hub bage](https://img.shields.io/badge/-GitHub-181717?logo=GitHub&style=for-the-badge)](https://github.com/Just1truc)
[![mail](https://img.shields.io/badge/-Mail-0078D4?logo=Microsoft-Outlook&style=for-the-badge)](mailto:justin.duc@epitech.eu)

#### Architecture Designer : Mathias André

[![linkeding bage](https://img.shields.io/badge/-linkedin-0A66C2?logo=linkedin&style=for-the-badge)](https://www.linkedin.com/in/mathias-andré/)
[![git hub bage](https://img.shields.io/badge/-GitHub-181717?logo=GitHub&style=for-the-badge)](https://github.com/MathiDEV)
[![mail](https://img.shields.io/badge/-Mail-0078D4?logo=Microsoft-Outlook&style=for-the-badge)](mailto:mathias.andre@epitech.eu)

#### Performances Responsible : Valentin Nouri

[![linkeding bage](https://img.shields.io/badge/-linkedin-0A66C2?logo=linkedin&style=for-the-badge)](https://www.linkedin.com/in/valentin-nouri/)
[![git hub bage](https://img.shields.io/badge/-GitHub-181717?logo=GitHub&style=for-the-badge)](https://github.com/vavarier)
[![mail](https://img.shields.io/badge/-Mail-0078D4?logo=Microsoft-Outlook&style=for-the-badge)](mailto:valentin.nouri@epitech.eu)

#### Quality Responsible : Thomas Mazaud

[![linkeding bage](https://img.shields.io/badge/-linkedin-0A66C2?logo=linkedin&style=for-the-badge)](https://www.linkedin.com/in/thomasmazaud/)
[![git hub bage](https://img.shields.io/badge/-GitHub-181717?logo=GitHub&style=for-the-badge)](https://github.com/Fyroeo)
[![mail](https://img.shields.io/badge/-Mail-0078D4?logo=Microsoft-Outlook&style=for-the-badge)](mailto:thomas.mazaud@epitech.eu)
