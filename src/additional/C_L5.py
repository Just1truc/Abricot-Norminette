import abricot
from utils import is_source_file
from utils import TYPES_TOKENS, KEYWORDS_TOKENS
from utils.functions import get_functions


def line_allow_declaration(tokens, line):
    for token in tokens:
        if token.line == line and token.name == 'for':
            return True
    return False


def check_multiple_declarations():
    for file in abricot.getSourceFileNames():
        if not is_source_file(file):
            continue
        tokens = abricot.getTokens(file, 1, 0, -1, -1, TYPES_TOKENS +
                                   ['assign', 'comma', 'newline', 'identifier'] + KEYWORDS_TOKENS)
        declaration_line = False
        assign_count = 0
        comma_count = 0
        for i, token in enumerate(tokens):
            if token.name == 'newline':
                declaration_line = False
                assign_count = 0
                comma_count = 0
                continue
            if token.name in TYPES_TOKENS and token.name != 'comma':
                if i == 0 or tokens[i - 1].name == 'newline':
                    declaration_line = True
                continue
            if token.name == 'comma' and declaration_line:
                comma_count += 1
            if token.name == 'assign' and declaration_line:
                assign_count += 1
            if assign_count > 1 and comma_count >= 1:
                abricot.report(file, token.line, 'L5')


def check_variable_declaration():
    for file in abricot.getSourceFileNames():
        if not is_source_file(file):
            continue
        functions = get_functions(file)
        for function in functions:
            if function.body is None:
                continue
            tokens = abricot.getTokens(file,
                                       function.body.line_start, function.body.column_start,
                                       function.body.line_end, function.body.column_end,
                                       TYPES_TOKENS + KEYWORDS_TOKENS + ['newline', 'identifier'])
            declaration = True
            for i, token in enumerate(tokens):
                if token.name in KEYWORDS_TOKENS:
                    declaration = False
                    continue
                if not declaration and token.name in TYPES_TOKENS and token.name != 'comma':
                    if i == 0 or tokens[i - 1].name == 'newline':
                        if not line_allow_declaration(tokens, token.line):
                            abricot.report(file, token.line, 'L5')


def checker():
    check_multiple_declarations()
    check_variable_declaration()
