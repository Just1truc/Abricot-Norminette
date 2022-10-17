import abricot

from utils import is_source_file, is_header_file, get_lines
from utils.functions import get_functions
from utils.functions.function import Function


def is_only_one_line_without_comment(file: str, last_function: Function, current_function: Function):
    try:
        tokens = abricot.getTokens(
            file,
            last_function.body.line_end + 1,
            last_function.body.column_end,
            current_function.prototype.line_start - 1,
            current_function.prototype.column_start + 1,
            ['ccomment', 'cppcomment']
        )
    # pylint:disable=W0703
    except Exception:
        return True

    if len(tokens) == 0:
        return False
    if tokens[0].line - last_function.body.line_end != 2:
        return False
    if (current_function.prototype.line_start - tokens[-1].line - tokens[-1].value.count('\n')) > 1:
        return False
    return True


def checker(config):
    for file in abricot.getSourceFileNames():
        if not is_source_file(file) and not is_header_file(file):
            continue

        lines = get_lines(file, replace_comments=True, replace_stringlits=True)

        functions = [f for f in get_functions(file) if f.body is not None]
        for i, f in enumerate(functions):
            if i == 0:
                continue
            end_last_function = functions[i - 1].body.line_end
            start_current_function = f.prototype.line_start
            if start_current_function - end_last_function < 2:
                abricot.report(file, start_current_function, 'G2')
            elif start_current_function - end_last_function == 2:
                if lines[f.prototype.line_start - 2] != '':
                    abricot.report(file, start_current_function, 'G2')
            elif i > 0 and not is_only_one_line_without_comment(file, functions[i - 1], functions[i]):
                abricot.report(file, start_current_function, 'G2')



