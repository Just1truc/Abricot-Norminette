import abricot

from utils import is_source_file, is_header_file


def checker(config):
    for file in abricot.getSourceFileNames():
        if not is_source_file(file) and not is_header_file(file):
            continue
        for goto_token in abricot.getTokens(file, 1, 0, -1, -1, ['goto']):
            abricot.report(file, goto_token.line, 'C3')



