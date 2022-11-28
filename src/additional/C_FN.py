import abricot
from utils import BINARY_OPERATORS_TOKENS, TYPES_TOKENS
from utils import is_source_file

banned_functions = [
    'printf',
    'puts',
    'scanf',
    'putchar',
    'strlen',
    'strcpy',
    'strcat',
    'strcmp',
    'strncpy',
    'strncat',
    'strncmp',
]

def check_file_functions(file):
    tokens = abricot.getTokens(
        file, 1, 0, -1, -1,
        ['identifier', 'leftparen'] + TYPES_TOKENS + BINARY_OPERATORS_TOKENS
    )
    for i, token in enumerate(tokens):
        if token.name != 'identifier':
            continue
        if token.value not in banned_functions:
            continue
        if i != 0 and tokens[i - 1].name in TYPES_TOKENS:
            continue
        if i + 1 >= len(tokens) or tokens[i + 1].name != 'leftparen':
            continue
        abricot.report(file, token.line, 'FN')

def check_banned_functions():
     for file in abricot.getSourceFileNames():
        if not is_source_file(file):
            continue
        check_file_functions(file)


def checker():
    check_banned_functions()
