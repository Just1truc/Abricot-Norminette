import abricot

from utils import is_source_file, is_header_file
from utils.functions import get_functions


def checker(config):
    for file in abricot.getSourceFileNames():
        if not is_source_file(file) and not is_header_file(file):
            continue
        functions = get_functions(file)

        for function in functions:
            last_function_token = function.prototype if function.body is None else function.body
            comments = abricot.getTokens(file, function.prototype.line_start, function.prototype.column_start,
                                      last_function_token.line_end, last_function_token.column_end,
                                      ['ccomment', 'cppcomment'])
            for comment in comments:
                abricot.report(file, comment.line, "F8")



