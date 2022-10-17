import abricot
from utils import is_source_file, is_header_file
from utils.functions import get_functions

MAX_BODY_LINE_COUNT = 20

def checker(config):
    for file in abricot.getSourceFileNames(config):
        if not is_source_file(file) and not is_header_file(file):
            continue
        functions = get_functions(file)
        for function in functions:
            if function.body is None:
                continue
            lines = function.body.raw[1:-1].split('\n')
            if len(lines) > 0 and lines[0] is not None and len(lines[0]) == 0:
                lines = lines[1:]
            if len(lines) > 0 and lines[-1] is not None and len(lines[-1]) == 0:
                lines = lines[:-1]
            for i in range(0, len(lines) - MAX_BODY_LINE_COUNT):
                abricot.report(file, function.body.line_end - i - 1, "F4")


