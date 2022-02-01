import os
import sys
import os.path
from os import path
import re

class Check_Goto:
    def __init__(self):
        self.auth = True

    def run(self, Norm_obj, files):
        inside = open(files, "r")
        line = 0
        for lines in inside:
            line += 1
            if " goto " in lines and self.auth == True:
                Norm_obj.major.append("[MAJOR]: [C3]: Cringe t'as un goto fdf: line : " + str(line))
        inside.close()

class Line_Break:
    def __init__(self):
        self.active = True
    
    def run(self, Norm_obj, file_name):
        if self.active == True:
            inside = open(file_name, "r")
            rest = ""
            for lines in inside:
                rest = lines
                if not("\n" in lines):
                    Norm_obj.info.append("[INFO]: [A3]: Line break missing at end of file")
            inside.close()

class Check_include:
    def __init__(self):
        self.active = True

    def run(self, Norm_obj, files):
        if self.active == True:
            inside = open(files, "r")
            line = 0
            in_it = 0
            for lines in inside:
                line += 1
                if "#include" in lines:
                    if ('"' in lines):
                        tab = lines.split('"')
                        if tab[1][-1] != 'h' or tab[1][-2] != '.':
                            Norm_obj.major.append("[MAJOR]: [G6]: #include should only contain .h files : line : " + str(line))
                    else:
                        tot = ""
                        for char in lines:
                            if char == '>':
                                in_it = 0
                            if in_it == 1:
                                tot += str(char)
                            if char == '<':
                                in_it = 1
                        if tot[-1] != 'h' or tot[-2] != '.':
                            Norm_obj.major.append("[MAJOR]: [G6]: #include should only contain .h files : line : " + str(line))
            inside.close()

class Misplaced_spaces:
    def __init__(self):
        self.active = True
    
    def tabs_to_space(self, string):
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

    def fix_clang(self, string):
        return string.replace(" ;", ";")

    def run(self, Norm_obj, files):
        if ".c" in files and self.active == True:
            files = [files]
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
                        pos += 1
                        if (pos in break_pos):
                            fmt = fmt[:i + 1] + '\n' + fmt[i + 1:]
                    i += 1
                fmt = str(fmt).splitlines()
                lines = lines.splitlines()
                for i in range(min(len(lines), len(fmt))):
                    clean_fmt = self.fix_clang(self.tabs_to_space(fmt[i])).strip()
                    clean_line = lines[i].rstrip('\\').strip()
                    if clean_fmt != clean_line and clean_fmt.replace(' ', '') == clean_line.replace(' ', '') and clean_line[0:2] != "**":
                        Norm_obj.minor.append("[MINOR]: [L3]: misplaced spaces: line :" + str(i + 1))
                file_opened.close()

class Too_many_functions:
    def __init__(self):
        self.max_function_nbr = 5
        self.active = True

    def run(self, Norm_obj, files):
        if (files[-1] == 'c' and files[-2] == '.') and self.active == True:
            inside = open(files, "r")
            function_nbr = 0
            for lines in inside:
                if (lines[0] == '{'):
                    function_nbr += 1
            if (function_nbr > self.max_function_nbr):
                Norm_obj.major.append("[MAJOR]: [03]: Too many functions in one file : ( " + str(function_nbr) + " > 5 )")
            inside.close()

class Include_guard:
    def __init__(self):
        self.check_ifndef = 0
        self.check_endif = 0

    def run(self, Norm_obj, files):
        if (files[-1] == 'h' and files[-2] == '.'):
            buffer = open(files, "r")
            for lines in buffer:
                if "#ifndef" in lines:
                    self.check_ifndef = 1
                if "#endif" in lines:
                    self.check_endif = 1
            buffer.close()
            if (self.check_ifndef == 0 or self.check_endif == 0):
                Norm_obj.minor.append("[MINOR]: [H2]: Header not protected from double inclusion")


class Too_many_depth:
    def __init__(self):
        self.max_depth = 3
        self.indentation_space_nbr = 4
        self.active = True

    def run(self, Norm_obj, files):
        if self.active == True:
            tot = 1
            spaces_lvl = 4
            depth = 1
            op_list = [ "for (", "for(", "if (", "if(", "while (", "while(", "do(", "do (" ]
            inside = open(files, "r")
            line = 0
            for lines in inside:
                line += 1
                in_it = 0
                i = 0
                while (lines[i] == ' '): i+=1
                for val in op_list:
                    if val in lines:
                        in_it = 1
                        break;
                if in_it == 1:
                    if i > spaces_lvl:
                        depth += 1
                        spaces_lvl = i
                    elif i < spaces_lvl:
                        depth = i // self.indentation_space_nbr
                        spaces_lvl = i
                    elif i == spaces_lvl and not("else if" in lines):
                        depth = i // self.indentation_space_nbr
                        spaces_lvl = i
                    if "else if" in lines:
                        depth += 1
                if depth >= self.max_depth and in_it == 1:
                    Norm_obj.major.append("[MAJOR]: [C1]: Conditionnal branching: line : "+str(line))                    
            inside.close()

class Arguments_nbr:
    def __init__(self):
        self.max_arguments_nbr = 4
        self.active = True

    def run(self, Norm_obj, files):
        if self.active == True:
            inside = open(files, "r")
            line = 0
            counter = 0
            last_char = 'p'
            for lines in inside:
                line += 1
                for char in lines:
                    if (char == '(' and lines[0] != ' '):
                        counter = 1
                    if (counter > 0 and char == ','):
                        counter += 1
                    if (char == ')' and lines[0] != ' '):
                        if (counter > self.max_arguments_nbr):
                            Norm_obj.major.append("[MAJOR]: [F5]: Function should not need more than 4 arguments: line :" + str(line) +" ( "+ str(counter)+ " > 4 )")
                        if last_char == '(':
                            Norm_obj.major.append("[MAJOR]: [F5]: Argumentless functions should take void as parameter: line :" + str(line))
                        counter = 0
                    last_char = char
            inside.close()

class Function_length:
    def __init__(self):
        self.max_length = 20
        self.active = True
    
    def run(self, Norm_obj, files):
        if self.active == True:
            inside = open(files, "r")
            counter = 0
            begin_line = 0
            line = 0
            if (".c" in files):
                for lines in inside:
                    line += 1
                    if (lines[0] == '{'):
                        counter = 1
                        begin_line = line
                    if (counter > 0):
                        counter += 1
                    if (lines[0] == '}'):
                        if (counter - 3 > self.max_length):
                            Norm_obj.major.append("[MAJOR]: [F4]: A function should not exceed 20 lines: line :" + str(begin_line) + " ( " + str(counter - 3) + " > 20 )")
                        counter = 0
            inside.close()

class Curly_brackets:
    def __init__(self):
        self.active = True

    def check_c_files(self, Norm_obj, files):
        inside = open(files, "r")
        line = 0
        prev_line = "02"
        for lines in inside:
            line += 1
            if (lines[0] != ' ' and lines[0] != '\n' and "(" in lines and ")" in lines and "{" in lines):
                Norm_obj.minor.append("[MINOR]: [L4]: Curly brackets misplaced: line :" + str(line))
            if (lines[0] == ' ' and "{" in lines and not("if" in lines) and not("else" in lines) and not("for" in lines) and not("while" in lines) and not(")" in lines) and not("}" in lines)) and not("do" in lines):
                Norm_obj.minor.append("[MINOR]: [L4]: Curly brackets misplaced: line :" + str(line))
            if (prev_line[0] == ' ' and "}" in prev_line and not("if" in prev_line) and not("else" in prev_line) and not("for" in prev_line) and not("while" in prev_line) and "else" in lines and not("}" in lines)):
                Norm_obj.minor.append("[MINOR]: [L4]: Curly brackets misplaced: line :" + str(line))
            prev_line = lines
        inside.close()

    def check_h_files(self, Norm_obj, files):
        inside = open(files, "r")
        line = 0
        prev_line = "02"
        for lines in inside:
            line += 1
            if "{" in lines and "struct" in prev_line:
                Norm_obj.minor.append("[MINOR]: [L4]: Curly brackets misplaced: line :" + str(line))
            prev_line = lines
        inside.close()

    def run(self, Norm_obj, files):
        if self.active == True:
            if ".c" in files:
                self.check_c_files(Norm_obj, files)
            if ".h" in files:
                self.check_h_files(Norm_obj, files)

class Identation_error:
    def __init__(self):
        self.active = True

    def run(self, Norm_obj, files):
        if self.active == True:
            inside = open(files, "r")
            test = 0
            for lines in inside:
                test += 1
                for char in lines:
                    if (char == '\t' and ("Makefile" in files) != True):
                        Norm_obj.minor.append("[MINOR]: [L2]: No tab should be replaced by an identation: line :" + str(test))
            inside.close()

class Trailling_spaces:
    def __init__(self):
        self.active = True

    def run(self, Norm_obj, files):
        if self.active == True:
            inside = open(files, "r")
            line = 0
            for lines in inside:
                line += 1
                if len(lines) >= 2:
                    if lines[-1] == '\n' and lines[-2] == ' ':
                        Norm_obj.minor.append("[MINOR]: [G8]: Trailling space: line : "+ str(line))
            inside.close()

class Line_Endings:
    def __init__(self):
        self.forbidden_endings = [ '\r' ]
        self.active = True

    def run(self, Norm_obj, files):
        if ".c" in files and self.active == True:
            inside = open(files, "r")
            line = 0
            for lines in inside:
                line += 1
                for endings in self.forbidden_endings:
                    if endings == lines[-1]:
                        Norm_obj.minor.append("[MINOR]: [G7]: Line should finish only end with a \n: line:"+ str(line))
            inside.close()
    
class Global_variable:

    def __init__(self):
        self.var_types = [ "int", "char", "float", "double", "void"]
        self.active = True
        self.get_struct(os.listdir("."), ".")

    def get_struct(self, direct, paths):
        for files in direct:
            test = paths + "/" + files
            if path.isdir(test):
                self.get_struct(os.listdir(test), test)
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
                            tot=lines.replace(" ", "").replace("}", "").replace(";\n", "").replace("\n", "")
                            if len(tot) > 0:
                                self.var_types += [tot]

    def run(self, Norm_obj, files):
        if ".c" in files and self.active == True:
            inside = open(files, "r")
            line = 0
            for lines in inside:
                line += 1
                for types in self.var_types:
                    if types in lines and not("const" in lines) and not("(" in lines) and lines[0] != ' ' and lines[0] != '\t' and not(")" in lines) and not(lines[0:2] == "**"):
                        Norm_obj.minor.append("[MINOR]: [G4]: Global variable should be const: line:"+ str(line))
            inside.close()

class Preprocessor_Directives:
    def __init__(self):
        self.active = True

    def run(self, Norm_obj, files):
        start=0
        line = 0
        inside = open(files, "r")
        if (".h" in files and files[-1] == 'h') and self.active == True:
            for lines in inside:
                line += 1
                if "#ifndef" in lines:
                    start=1
                if "#endif" in lines:
                    start = 0
                if "#endif" in lines or "#ifndef" in lines:
                    if lines[0] != '#':
                        Norm_obj.minor.append("[MINOR]: [G3]: preprocessor directives should be indented: line:"+ str(line))
                if ("#define" in lines or "#include" in lines) and start == 1:
                    i = 0
                    while (lines[i] == ' '):
                        i += 1
                    if (i != 4):
                        Norm_obj.minor.append("[MINOR]: [G3]: preprocessor directives should be indented: line:"+ str(line))
        inside.close()

class Empty_line:
    def __init__(self):
        self.active = True

    def run(self, Norm_obj, files):
        inside = open(files, "r")
        trailling_lines = 0
        line_nbr = 0
        if (".c" in files) and self.active == True:
            for lines in inside:
                line_nbr += 1
                if (lines == "\n"):
                    trailling_lines += 1
                else:
                    trailling_lines = 0
                if (trailling_lines == 2):
                    trailling_lines = 0
                    Norm_obj.minor.append("[MINOR]: [G2]: There should be only one empty_line each time: line:" + str(line_nbr))                                                          
        inside.close()
        inside = open(files, "r")
        prev_line = "\n"
        line = 0
        if (".c" in files) and self.active == True:
            for lines in inside:
                line += 1
                if prev_line[0] == '}' and lines[0] != '\n':
                    Norm_obj.minor.append("[MINOR]: [G2]: There should be only one empty_line each time: line:" + str(line_nbr))                                                              
                prev_line = lines
        inside.close()
    
class Check_file_header:

    def __init__(self):
        self.c_file_header = "/*\n** EPITECH PROJECT,\n** File description:\n*/\n"
        self.h_file_header = "##\n## EPITECH PROJECT,\n## File description:\n##\n"
        self.active = True
    
    def run(self, Norm_obj, files):
        if self.active == True:
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
                if (result != self.c_file_header):
                    Norm_obj.major.append("[MAJOR]: [G1]: File header not correct")
            if (files == "Makefile"):
                if (result != self.h_file_header):
                    Norm_obj.major.append("[MAJOR]: [G1]: File header not correct")
            inside.close()

class Check_Include:

    def __init__(self):
        self.authorised_files = [ ".h" ]
        self.active = True

    def run(self, files):
        if self.active == True:
            tot = []
            for dos in os.listdir(files):
                if ((".h" in dos) != True):
                    tot.append("\033[91m[MAJOR]: [G6]: Include folder should only contain .h files: " + dos.replace("./", ""))
            if len(tot) > 0:
                er = 1
                print("\033[1;36mIn include\n")
                for i in tot:
                    print(i)
                print("")

class Check_file:
    def __init__(self):
        self.forbidden_files = [ ".o", ".gch", ".a", ".so", "~", "#", ".d" ]
        self.active = True

    def check_04(self, file_name, path, Norm_obj):
        if (any(ele.isupper() for ele in str(file_name)) == True and ("Makefile" in file_name) != True) and self.active == True:
            Norm_obj.bad_files.append(str("[MAJOR]: [O4]: Name not in snake case convention: " + str(path.replace("./", ""))))

    def check_01(self, file_name, files, Norm_obj):
        for ext in self.forbidden_files:
            if (ext in str(files) and files[len(files) - 1] == ext[len(ext) - 1]):
                Norm_obj.bad_files.append(str("[MAJOR]: [O1]: Delivery Folder should not contain "+ ext +" files: " + files.replace("./", "")))
            
    def run(self, file_name, path, Norm_obj):
        if self.active == True:
            self.check_04(file_name, path, Norm_obj)
            self.check_01(file_name, path, Norm_obj)
    
class Too_Long_Line:
    def __init__(self):
        self.line_length = 80
        self.attributes = {"line_length" : self.line_length}
        self.active = True

    def run(self, Norm_obj, files):
        if self.active == True:
            inside = open(files, "r")
            line = 0
            for lines in inside:
               line += 1
               if len(lines) > self.line_length:
                   Norm_obj.major.append("[MAJOR]: [F3]: The length of a line should not exceed 80 columns: line : "+ str(line) + " ( " + str(len(lines)) +" > "+ str(self.line_length) + " )")
            inside.close()

class Norms:
    ### Norms class: Central hub of the error handling
    def __init__(self):
        self.norm_list = {"Too long line" : Too_Long_Line(),
                          "Check file header" : Check_file_header(),
                          "Empty line" : Empty_line(),
                          "Preprocessor_Directives" : Preprocessor_Directives(),
                          "Global Variable" : Global_variable(),
                          "Line_Endings" : Line_Endings(),
                          "Trailling_spaces" : Trailling_spaces(),
                          "Identation_error" : Identation_error(),
                          "Curly_brackets" : Curly_brackets(),
                          "Function_length" : Function_length(),
                          "Arguments_nbr" : Arguments_nbr(),
                          "Too_many_functions" : Too_many_functions(),
                          "Misplaced_spaces" : Misplaced_spaces(),
                          "Too_many_depth" : Too_many_depth(),
                          "Line_Break" : Line_Break(),
                          "Check_include" : Check_include(),
                          "Check_Goto" : Check_Goto(),
                          "Include Guard" : Include_guard()}
        self.organisation_norms = Check_file()
        self.major = []
        self.minor = []
        self.info = []
        self.bad_files = []
        self.error_nbr = 0
        self.minor_color = "\033[93m"
        self.major_color = "\033[91m"
        self.info_color = "\033[97m"

    def browse_directory(self, directory, paths):
        for files in directory:
            test = paths + "/" + files
            if path.isdir(test) and files != "tests":
                if (files == "include"):
                    inc = Check_Include()
                    inc.run(test)
                obj = self.organisation_norms
                obj.check_04(files, test, self)
                self.browse_directory(os.listdir(test), paths + "/" + str(files))
            else:
                if (".c" in files or ".h" in files or "Makefile" in files or ".o" in files):
                    obj = self.organisation_norms
                    obj.run(files, paths + "/" + files, self)
                    if ((files[-1] == 'c' and files[-2] == '.') or "Makefile" in files or (files[-1] == 'h' and files[-2] == '.')) and not("~" in files) and not(".swp" in files) and files.replace("./", "")[0] != '.':
                        for rules in self.norm_list:
                            obj = self.norm_list[rules]
                            obj.run(self, paths + "/" + files)
                    if (len(self.major) != 0 or len(self.minor) != 0 or len(self.info) != 0):
                        self.error_nbr += 1
                        print("\033[1;36mIn File", test.replace("./", ""), "\n")
                        for i in self.major:
                            print(self.major_color + i)
                        for i in self.minor:
                            print(self.minor_color + i)
                        for i in self.info:
                            print(self.info_color + i)
                        print("")
                    self.major = []
                    self.minor = []
                    self.info = []

    def run(self):
        os.system("echo \"BasedOnStyle: LLVM\nAccessModifierOffset: -4\nAllowShortIfStatementsOnASingleLine: Never\nAlignAfterOpenBracket: DontAlign\nAlignOperands: false\nAllowShortCaseLabelsOnASingleLine: true\nContinuationIndentWidth: 0\nBreakBeforeBraces: Linux\nColumnLimit: 0\nAllowShortBlocksOnASingleLine: Never\nAllowShortFunctionsOnASingleLine: None\nFixNamespaceComments: false\nIndentCaseLabels: false\nIndentWidth: 4\nNamespaceIndentation: All\nTabWidth: 4\nUseTab: Never\nSortIncludes: true\nIncludeBlocks: Preserve\" > .clang-format")
        self.browse_directory(os.listdir("."), ".")
        os.system("rm .clang-format")
        if len(self.bad_files) > 0:
            self.error_nbr += 1
            print("\033[1;36mBad files :\n")
            for i in self.bad_files:
                print(self.major_color + i)
            print("")
        if self.error_nbr == 0:
            print("\033[1;32mNo Coding style error detected : Code clean")

        
def main():
    rule = Norms()
    rule.run()

main()
