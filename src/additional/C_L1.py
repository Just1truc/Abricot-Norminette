import abricot
from utils import is_source_file, is_header_file

NO_DECLARATION_STATEMENTS = ['if', 'while', 'case']
NOT_ON_STATEMENT_LINE = ['assign', 'return', 'continue', 'break']


def line_allow_exceptions(tokens, line):
    for token in tokens:
        if token.line == line and token.name == 'for':
            return True
    return False


def check_multiple_assignement():
    for file in abricot.getSourceFileNames():
        if not is_source_file(file) and not is_header_file(file):
            continue
        tokens = abricot.getTokens(file, 1, 0, -1, -1, ['assign', 'newline', 'semicolon', 'for'])
        assign_count = 0
        semicolon_count = 0
        for token in tokens:
            if token.name == 'newline':
                assign_count = 0
                semicolon_count = 0
                continue
            if line_allow_exceptions(tokens, token.line):
                continue
            if token.name == 'assign':
                assign_count += 1
            if token.name == 'semicolon':
                semicolon_count += 1
            if assign_count > 1 or semicolon_count > 1:
                abricot.report(file, token.line, 'L1')

def check_statement_and_declaration():
    for file in abricot.getSourceFileNames():
        if not is_source_file(file) and not is_header_file(file):
            continue
        tokens = abricot.getTokens(file, 1, 0, -1, -1, ['newline'] + NOT_ON_STATEMENT_LINE + NO_DECLARATION_STATEMENTS)
        statement = False
        for token in tokens:
            if token.name == 'newline':
                statement = False
                continue
            if token.name in NO_DECLARATION_STATEMENTS:
                statement = True
                continue
            if token.name in NOT_ON_STATEMENT_LINE and statement:
                abricot.report(file, token.line, 'L1')


def checker():
    check_multiple_assignement()
    check_statement_and_declaration()
