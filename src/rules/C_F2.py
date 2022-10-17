import abricot
from utils import is_source_file, is_header_file, is_lower_snakecase
from utils.functions import get_functions


def checker(config):
    for file in abricot.getSourceFileNames():
        if not is_source_file(file) and not is_header_file(file):
            continue
        functions = get_functions(file)
        for function in functions:
            if function.body is None:
                continue
            if not is_lower_snakecase(function.name) or len(function.name.replace('_', '')) <= 2:
                abricot.report(file, function.prototype.line_start, "F2")



