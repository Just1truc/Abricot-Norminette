import re

import abricot
from utils import is_source_file, is_header_file, get_lines

FORBIDDEN_SOURCE_FILE_DIRECTIVES = ['typedef', 'pp_define']

def checker(config):
    for file in abricot.getSourceFileNames(config):
        if not is_source_file(file) and not is_header_file(file):
            continue
        s = ""
        for line in get_lines(file):
            s += line
            s += "\n"
        p = re.compile(r"^[\t ]*(?P<modifiers>(?:(?:inline|static|unsigned|signed|short|long|volatile|struct)[\t ]+)*)"
                       r"(?!else|typedef|return)(?P<type>\w+)\**[\t ]+\**[\t ]*\**[\t ]*(?P<name>\w+)(?P<spaces>[\t ]*)"
                       r"\((?P<parameters>[\t ]*"
                       r"(?:(void|(\w+\**[\t ]+\**[\t ]*\**\w+[\t ]*(,[\t \n]*)?))+|)[\t ]*)\)[\t ]*"
                       r"(?P<endline>;\n|\n?{*\n){1}", re.MULTILINE)
        for search in p.finditer(s):
            line_start = s.count('\n', 0, search.start()) + 1
            if is_source_file(file):
                if search.group('endline') and search.group('modifiers'):
                    is_static_inline = 'static' in search.group('modifiers') and 'inline' in search.group('modifiers')
                    if is_static_inline and is_source_file(file):
                        abricot.report(file, line_start, "H1")
            elif is_header_file(file) and search.group('endline') and '{' in search.group('endline') \
                    and 'static' not in search.group('modifiers') and 'inline' not in search.group('modifiers'):
                abricot.report(file, line_start, "H1")
    for file in abricot.getSourceFileNames(config):
        if not is_source_file(file):
            continue
        for token in abricot.getTokens(file, 1, 0, -1, -1, FORBIDDEN_SOURCE_FILE_DIRECTIVES):
            abricot.report(file, token.line, 'H1')







