import abricot
from utils import is_header_file, is_source_file
from utils.functions import get_functions

MAX_FUNCTION_COUNT = 5

def checker(config):
    for file in abricot.getSourceFileNames(config):
        if not is_source_file(file) and not is_header_file(file):
            continue

        functions = get_functions(file)
        function_count = 0
        for function in functions:
            if function.body is None:
                continue
            function_count += 1
            if function_count > MAX_FUNCTION_COUNT:
                abricot.report(file, function.prototype.line_start, "O3")


