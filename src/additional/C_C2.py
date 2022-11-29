import abricot
from utils import is_header_file, is_source_file

def check_chained_ternaries():
    for file in abricot.getSourceFileNames():
        if not is_source_file(file) and not is_header_file(file):
            continue
        tokens = abricot.getTokens(
            file, 1, 0, -1, -1, ['colon', 'newline', 'question_mark'])
        semi_colon_count = 0
        line = 1
        is_ternary = False
        for token in tokens:
            if token.name == 'newline':
                line += 1
                semi_colon_count = 0
                is_ternary = False
                continue
            if token.name == 'question_mark':
                is_ternary = True
            if is_ternary and token.name == 'colon':
                semi_colon_count += 1
            if semi_colon_count == 2:
                abricot.report(file, line, 'C2')

def checker():
    check_chained_ternaries()
