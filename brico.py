import os
import sys
import os.path
from os import path
import re

def tabs_to_space(string):
    begin = 0
    len_str = len(string)
    if len_str == 0:
        return (string)
    while string[begin] == ' ':
        begin += 1
    if begin == len_str - 1:
        return (string)
    string = string[begin:]
    while re.search(r'(\s\s)+(?=([^"]*"[^"]*")*[^"]*$)', string):
        string = re.sub(r'(\s\s)+(?=([^"]*"[^"]*")*[^"]*$)', ' ', string)
    return (' ' * begin + string)

def fix_clang(string):
    return string.replace(" ;", ";")

def misplaced_spaces(files):
    global minor
    for f in files:
        break_pos = []
        file_opened = open("./"+f, 'r')
        lines = file_opened.read()
        absolute_lines = lines.replace(' ', '').replace('\\\n', '\n')
        for i in range(len(absolute_lines)):
            if absolute_lines[i] == '\n':
                break_pos.append(i)
        fmt = os.popen("clang-format "+f).read().replace('\n', '')
        pos = 0
        i = 0
        while i < len(fmt):
            if fmt[i] != ' ':
                pos += 1;
                if (pos in break_pos):
                    fmt = fmt[:i + 1] + '\n' + fmt[i + 1:]
            i += 1
        fmt = str(fmt).splitlines()
        lines = lines.splitlines()
        for i in range(min(len(lines), len(fmt))):
            clean_fmt = fix_clang(tabs_to_space(fmt[i])).strip()
            clean_line = lines[i].rstrip('\\').strip()
            if clean_fmt != clean_line and clean_fmt.replace(' ', '') == clean_line.replace(' ', ''):
                minor.append("\033[1;33;40m[MINOR]: [L3]: misplaced spaces: line :" + str(i + 1))

def check_include(files):
    tot = []
    for dos in files:
        if ((".h" in dos) != True):
            tot.append("\033[1;31;40m[MAJOR]: [G6]: Include folder should only contain .h files: " + dos.replace("./", ""))
            #print("\033[1;31;40m[MAJOR]: [G6]:    Include folder should only contain .h files:   ", dos)
    if len(tot) > 0:
        er = 1
        print("\033[1;36mIn include\n")
        for i in tot:
            print(i)
        print("")

def check_control_structure(files):
    global major
    global minor
    depth = 4
    tot = 1
    op_list = [ "for (", "for(", "if (", "if(", "while (", "while(" ]
    inside = open(files, "r")
    line = 0
    for lines in inside:
        line += 1;
        for val in op_list:
            if val in lines and "            " in lines:
                minor.append("\033[1;33;40m[MINOR]: [C1]: There should not be more than 3 depth: line :" + str(line))
                #print("\033[1;33;40m[MINOR]: [C1]:      There should not be more than 3 depth:     ", files, "line :", line)

def check_layout_inside_function(files):
    global major
    global minor
    inside = open(files, "r")
    line = 0
    test = 0;
    index = 0
    for lines in inside:
        test += 1
        for char in lines:
            if (char == '\t' and ("Makefile" in files) != True):
                minor.append("\033[1;33;40m[MINOR]: [L2]: No tab should be replaced by an identation: line :" + str(test))
                #print("\033[1;33;40m[MINOR]: [L2]:     No tab should be replaced by an identation:   ", files, "line :", test)
    inside.close()
    if ".c" in files:
        misplaced_spaces([files]);
    if ".c" in files:
        inside = open(files, "r")
        line = 0
        prev_line = "02"
        for lines in inside:
            line += 1
            if (lines[0] != ' ' and lines[0] != '\n' and "(" in lines and ")" in lines and "{" in lines):
                minor.append("\033[1;33;40m[MINOR]: [L4]: Curly brackets misplaced: line :" + str(line))
                #print("\033[1;33;40m[MINOR]: [L4]:              Curly brackets misplaced:            ", files, "line :", line)
            if (lines[0] == ' ' and "{" in lines and not("if" in lines) and not("else" in lines) and not("for" in lines) and not("while" in lines) and not(")" in lines) and not("}" in lines)):
                minor.append("\033[1;33;40m[MINOR]: [L4]: Curly brackets misplaced: line :" + str(line))
                #print("\033[1;33;40m[MINOR]: [L4]:              Curly brackets misplaced:            ", files, "line :", line)
            if (prev_line[0] == ' ' and "}" in prev_line and not("if" in prev_line) and not("else" in prev_line) and not("for" in prev_line) and not("while" in prev_line) and "else" in lines and not("}" in lines)):
                minor.append("\033[1;33;40m[MINOR]: [L4]: Curly brackets misplaced: line :" + str(line))
                #print("\033[1;33;40m[MINOR]: [L4]:              Curly brackets misplaced:            ", files, "line :", line)
            prev_line = lines
        inside.close()
            
def check_function(files):
    global major
    global minor
    inside = open(files, "r")
    line = 0
    for lines in inside:
        line += 1
        if len(lines) > 80:
            major.append("\033[1;31;40m[MAJOR]: [F3]: The length of a line should not exceed 80 columns: line : "+ str(line) + " ( " + str(len(lines)) +" > 80 )")
            #print("\033[1;31;40m[MAJOR]: [F3]: The length of a line should not exceed 80 columns:", files, "line :", line, "(", len(lines), "> 80 )")
    inside.close()
    inside = open(files, "r")
    counter = 0
    begin_line = 0
    line = 0;
    if (".c" in files):
        for lines in inside:
            line += 1
            if (lines[0] == '{'):
                counter = 1
                begin_line = line
            if (counter > 0):
                counter += 1
            if (lines[0] == '}'):
                if (counter - 3 > 20):
                    major.append("\033[1;31;40m[MAJOR]: [F4]: A function should not exceed 20 lines: line :" + str(begin_line) + " ( " + str(counter - 3) + " > 20 )")
                    #print("\033[1;31;40m[MAJOR]: [F4]:       A function should not exceed 20 lines:      ", files, "line :", begin_line, "(", counter - 3, "> 20 )")
                counter = 0
    inside.close()
    inside = open(files, "r")
    line = 0
    counter = 0
    for lines in inside:
        line += 1
        for char in lines:
            if (char == '(' and lines[0] != ' '):
                counter = 1
            if (counter > 0 and char == ','):
                counter += 1
            if (char == ')'):
                if (counter > 4):
                    major.append("\033[1;31;40m[MAJOR]: [F5]: Function should not need more than 4 arguments: line :" + str(line) +" ( "+ str(counter)+ " > 4 )")
                    #print("\033[1;31;40m[MAJOR]: [F5]:   Function should not need more than 4 arguments: ", files, "line :", line,"(", counter, "> 4 )")
                counter = 0
    inside.close()
            
def check_global_scope(files):
    global major
    global minor
    global var_types
    inside = open(files, "r")
    line_nbr = 0
    result = ""
    mid_res = ""
    for line in inside:
        if (line_nbr > 5):
            break
        if (line_nbr != 2 and line_nbr != 4):
            if (line_nbr == 1):
                for char in line:
                    mid_res += char
                    if (char == ','):
                        break
                mid_res += "\n"
                result += mid_res
            else:
                result += line
        line_nbr += 1
    if (".c" in  files):
        if (result != "/*\n** EPITECH PROJECT,\n** File description:\n*/\n"):
            major.append("\033[1;31;40m[MAJOR]: [G1]: File header not correct")
            #print("\033[1;31;40m[MAJOR]: [G1]:              File header not correct:             ", files)
    if (files == "Makefile"):
        if (result != "##\n## EPITECH PROJECT,\n## File description:\n##\n"):
            major.append("\033[1;31;40m[MAJOR]: [G1]: File header not correct")
            #print("\033[1;31;40m[MAJOR]: [G1]:              File header not correct:             ", files)
    inside.close()
    inside = open(files, "r")
    trailling_lines = 0;
    line_nbr = 0
    if (".c" in files):
        for lines in inside:
            line_nbr += 1
            if (lines == "\n"):
                trailling_lines += 1
            else:
                trailling_lines = 0
            if (trailling_lines == 2):
                trailling_lines = 0;
                minor.append("\033[1;33;40m[MINOR]: [G2]: There should be only one empty_line each time: line:" + str(line_nbr))
                #print("\033[1;33;40m[MINOR]: [G2]:   There should be only one empty_line each time:  ", files, ": line:", line_nbr)
    inside.close()
    inside = open(files, "r")
    prev_line = "\n"
    line = 0
    if (".c" in files):
        for lines in inside:
            line += 1
            if prev_line[0] == '}' and lines[0] != '\n':
                minor.append("\033[1;33;40m[MINOR]: [G2]: There should be only one empty_line each time: line:" + str(line_nbr))
                #print("\033[1;33;40m[MINOR]: [G2]:   There should be only one empty_line each time:  ", files, ": line:", line)
            prev_line = lines
    inside.close()
    line = 0
    start = 0
    inside = open(files, "r")
    if (".h" in files and files[-1] == 'h'):
        for lines in inside:
            line += 1
            if "#ifndef" in lines:
                start=1
            if "#endif" in lines:
                start = 0
            if ("#define" in lines or "#include" in lines) and start == 1:
                i = 0
                while (lines[i] == ' '):
                    i += 1
                if (i != 4):
                    minor.append("\033[1;33;40m[MINOR]: [G3]: preprocessor directives should be indented: line:"+ str(line))
                    #print("\033[1;33;40m[MINOR]: [G3]:   preprocessor directives should be indented:    ", files, ": line:", line)
    inside.close()
    if ".c" in files:
        inside = open(files, "r")
        line = 0
        for lines in inside:
            line += 1
            for types in var_types:
                if types in lines and not("const" in lines) and not("(" in lines) and lines[0] != ' ' and lines[0] != '\t' and not(")" in lines) and not(lines[0:2] == "**"):
                    minor.append("\033[1;33;40m[MINOR]: [G4]: Global variable should be const: line:"+ str(line))
            if "\r" in lines:
                minor.append("\033[1;33;40m[MINOR]: [G7]: Line should finish only end with a \n: line:"+ str(line))
        inside.close()
    inside = open(files, "r")
    line = 0
    for lines in inside:
        line += 1
        index = 0
        for char in lines:
            if (char == ' ' and lines[index + 1] == '\n' and line > 7):
                minor.append("\033[1;33;40m[MINOR]: [G8]: Trailling space: line :"+ str(line))
                #print("\033[1;33;40m[MINOR]: [G8]:                  Trailling space:                 ", files, "line :", line)
            index += 1
    inside.close()

def check_04(file_name):
    global po_o
    if (any(ele.isupper() for ele in str(file_name)) == True and ("Makefile" in file_name) != True):
        po_o.append(str("\033[1;31;40m[MAJOR]: [O4]: Name not in snake case convention: " + str(file_name.replace("./", ""))))

def check_file_organization(files, file_name):
    global major
    global minor
    global po_o
    forbidden_files = [ ".o", ".gch", ".a", ".so", "~", "#", ".d" ]
    for ext in forbidden_files:
        if (ext in str(files) and files[len(files) - 1] == ext[len(ext) - 1]):
            po_o.append(str("\033[1;31;40m[MAJOR]: [O1]: Delivery Folder should not contain "+ ext +" files: " + files))
            #print("\033[1;31;40m[MAJOR]: [O1]:    Delivery Folder should not contain", ext,"files:   ", files)
    check_04(file_name)
    if (files[-1] == 'c' and files[-2] == '.'):
        inside = open(files, "r")
        function_nbr = 0
        for lines in inside:
            if (lines[0] == '{'):
                function_nbr += 1
        if (function_nbr > 5):
            major.append("\033[1;31;40m[MAJOR]: [03]: Too many functions in one file : ( " + str(function_nbr) + " > 5 )")
            #print("\033[1;31;40m[MAJOR]: [03]:          Too many functions in one file :         ", files, "(", function_nbr, "> 5 )")
        inside.close()

def check_coding_style(files, file_name):
    global major
    global minor
    global er
    major = []
    minor = []
    check_file_organization(files, file_name)
    if ((files[-1] == 'c' and files[-2] == '.') or "Makefile" in files or (files[-1] == 'h' and files[-2] == '.')) and not("~" in files) and not(".swp" in files):
        check_global_scope(files)
        check_function(files)
        check_layout_inside_function(files)
        check_control_structure(files)
    if (len(major) != 0 or len(minor) != 0):
        er = 1
        print("\033[1;36mIn", files.replace("./", ""), "\n")
        for i in major:
            print(i)
        for i in minor:
            print(i)
        print("")

def browse_directory(directory, paths):
    for files in directory:
        test = paths + "/" + files
        if path.isdir(test) and files != "tests":
            if (files == "include"):
                check_include(os.listdir(test))
            check_04(files)
            browse_directory(os.listdir(test), paths + "/" + str(files))
        else:
            if (".c" in files or ".h" in files or "Makefile" in files or ".o" in files):
                check_coding_style(paths + "/" + files, files)

def get_struct(direct, paths):
    global var_types
    for files in direct:
        test = paths + "/" + files
        if path.isdir(test):
            get_struct(os.listdir(test), test)
        else:
            if (test[-1] == 'h' and test[-2] == '.'):
                inside = open(test, "r")
                begin = 0
                for lines in inside:
                    if "typedef" in lines:
                        begin = 1
                    tot=lines.replace(" ", "")
                    if begin == 1 and tot[0] == '}':
                        i = 0
                        var_types += [lines.replace(" ", "").replace("}", "").replace(";\n", "")]
                            
def main():
    global po_o
    global er
    global var_types
    var_types = [ "int", "char", "float", "double", "void"]
    get_struct(os.listdir("."), ".")
    er = 0
    po_o = []
    directory = os.listdir(".")
    paths = "."
    browse_directory(directory, paths)
    os.system("echo \"BasedOnStyle: LLVM\nAccessModifierOffset: -4\nAllowShortIfStatementsOnASingleLine: Never\nAlignAfterOpenBracket: DontAlign\nAlignOperands: false\nAllowShortCaseLabelsOnASingleLine: true\nContinuationIndentWidth: 0\nBreakBeforeBraces: Linux\nColumnLimit: 0\nAllowShortBlocksOnASingleLine: Never\nAllowShortFunctionsOnASingleLine: None\nFixNamespaceComments: false\nIndentCaseLabels: false\nIndentWidth: 4\nNamespaceIndentation: All\nTabWidth: 4\nUseTab: Never\nSortIncludes: true\nIncludeBlocks: Preserve\" > .clang-format")
    if len(po_o) != 0:
        er = 1
        print("\033[1;36mBad Files:\n")
        for i in po_o:
            print(i)
    if er == 0:
        print("\033[1;32mNo Coding style error detected : Code clean")
    os.system("rm .clang-format")

main()
