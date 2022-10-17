import abricot
from utils import is_source_file, is_header_file
from utils.functions import get_functions

MAX_ARGS_COUNT = 4


def checker(config):
    for file in abricot.getSourceFileNames():
        if not is_source_file(file) and not is_header_file(file):
            continue

        functions = get_functions(file)
        for function in functions:
            if len(function.arguments) == 0:
                abricot.report(file, function.prototype.line_start, "F6")



