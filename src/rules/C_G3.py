from typing import List

import abricot
from utils import is_header_file, get_lines, is_source_file


def _get_indentation_level(line: str):
    return len(line) - len(line.lstrip())


OPENING_DIRECTIVES = [
    'pp_if',
    'pp_ifdef',
    'pp_ifndef'
]

BRANCHING_DIRECTIVES = [
    'pp_elif',
    'pp_else'
]

CLOSING_DIRECTIVES = [
    'pp_endif'
]

ALL_DIRECTIVES = OPENING_DIRECTIVES + BRANCHING_DIRECTIVES + CLOSING_DIRECTIVES + [
    'pp_define',
    'pp_error',
    'pp_hheader',
    'pp_include',
    'pp_line',
    'pp_number',
    'pp_pragma',
    'pp_qheader',
    'pp_undef',
    'pp_warning'
]


def _is_pp_directive(file: str, line_number: int, directives: List[str]):
    token_list = abricot.getTokens(file, 1, 0, -1, -1, directives)
    return any(token.line == line_number for token in token_list)


def checker(config):
    for file in abricot.getSourceFileNames():
        if not is_header_file(file):
            continue

        lines = get_lines(file)
        previous_indentation_level_stack = [-1]
        for line_number, line in enumerate(lines, start=1):
            # Empty lines are ignored
            if len(line.strip()) == 0:
                continue

            line_indentation_level = _get_indentation_level(line)
            # If the indentation level is inferior to the current scope's, it is always an error
            if _is_pp_directive(file, line_number, ALL_DIRECTIVES) \
                    and line_indentation_level < previous_indentation_level_stack[-1]:
                abricot.report(file, line_number, 'G3')

            if _is_pp_directive(file, line_number, OPENING_DIRECTIVES):
                # When a opening directive is found,
                # its indentation level is pushed onto the stack and serves as the new reference
                previous_indentation_level_stack.append(line_indentation_level)
            elif _is_pp_directive(file, line_number, BRANCHING_DIRECTIVES):
                # When an adjacent branching directive is found,
                # it must be exactly on the same indentation level as its opening directive
                if line_indentation_level > previous_indentation_level_stack[-1]:
                    abricot.report(file, line_number, 'G3')
            elif _is_pp_directive(file, line_number, CLOSING_DIRECTIVES):
                # A closing directive must always be exactly on the same indentation level as what its opening directive
                if line_indentation_level > previous_indentation_level_stack[-1]:
                    abricot.report(file, line_number, 'G3')
                # Check done in order to prevent malformed #else directives to make this rule thrown an exception
                if len(previous_indentation_level_stack) >= 2:
                    previous_indentation_level_stack.pop()
            elif _is_pp_directive(file, line_number, ALL_DIRECTIVES) \
                    and line_indentation_level == previous_indentation_level_stack[-1]:
                # Directives inside directives that are not themselves branching directives
                # must always be indented more than the branching directive which contains it
                abricot.report(file, line_number, 'G3')



