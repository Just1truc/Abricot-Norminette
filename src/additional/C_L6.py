import abricot
from utils import is_source_file
from utils import TYPES_TOKENS
from utils.functions import get_functions


def assign_on_line(tokens, line):
    line_tokens = [tok for tok in tokens if tok.line == line and tok.name != 'star']
    if line_tokens[0].name == 'newline':
        return True
    if (len(line_tokens) < 2):
        return False
    if line_tokens[0].name in TYPES_TOKENS:
        return True
    if line_tokens[0].name == 'identifier' and line_tokens[1].name == 'identifier':
        if len(line_tokens) < 5:
            return True
        elif 'assign' in [tok.name for tok in line_tokens]:
            return True
    return False


def get_function_body(file, function):
    tokens = abricot.getTokens(file,
                               function.body.line_start, function.body.column_start,
                               function.body.line_end, function.body.column_end,
                               []
                               )
    tokens = [tok for tok in tokens if tok.name != 'space']
    if tokens[0].name == 'leftbrace':
        tokens = tokens[1:]
        if tokens[0].name == 'newline':
            tokens = tokens[1:]
    return tokens


def check_unwanted_linebreak():
    for file in abricot.getSourceFileNames():
        if not is_source_file(file):
            continue
        functions = get_functions(file)
        for function in functions:
            if function.body is None:
                continue
            tokens = get_function_body(file, function)
            declaration = True
            for i, token in enumerate(tokens):
                if declaration and not assign_on_line(tokens, token.line):
                    if i > 1 and (tokens[i - 1].name != 'newline' or tokens[i - 2].name != 'newline'):
                        abricot.report(file, token.line, 'L6')
                    declaration = False
                    continue
                if not declaration and token.name == 'newline':
                    if i != len(tokens) - 1 and tokens[i + 1].name == 'newline':
                        abricot.report(file, token.line + 1, 'L6')


def checker():
    check_unwanted_linebreak()
