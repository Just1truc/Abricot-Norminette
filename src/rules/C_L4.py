import re
from typing import List

import abricot
from utils import is_source_file, is_header_file, Token, get_lines
from utils.functions import get_functions
from utils.functions.function import Function


def get_function_start_at_token(functions: List[Function], token: Token) -> bool:
    for function in functions:
        if function.body and function.body.line_start == token.line and function.body.column_start == token.column:
            return function
    return None


# pylint:disable=too-many-branches
# pylint:disable=too-many-locals
# pylint:disable=too-many-statements
def checker(config):
    for file in abricot.getSourceFileNames():
        if not is_source_file(file) and not is_header_file(file):
            continue
        tokens_filter = [
            'leftbrace',
            'rightbrace',
            "case",
            "do",
            "else",
            "for",
            "if",
            "typedef",
            "switch",
            "while",
            "struct",
            "leftparen",
            "rightparen",
            "enum",
            "assign",
            "union",
            "identifier",
            "semicolon"
        ]
        lines = get_lines(file, True, True)
        tokens = abricot.getTokens(file, 1, 0, -1, -1, tokens_filter)
        tokens_count = len(tokens)
        do_while_braces_count = []
        enum_braces_count = []
        union_braces_count = []
        assign_braces_count = []
        struct_braces_count = []
        typedef_struct_braces_count = []
        functions = get_functions(file)
        skipping_level_increase_token = None
        skipping_level_decrease_token = None
        skipping_checks = False
        skipping_level = 0

        for i, token in enumerate(tokens):
            token_line_content = abricot.getLine(file, token.line)

            if not skipping_checks:
                if token.name == 'leftparen':
                    skipping_level = 1
                    skipping_checks = True
                    skipping_level_increase_token = 'leftparen'
                    skipping_level_decrease_token = 'rightparen'
                    continue
                if i > 0 and token.name == 'leftbrace' and tokens[i - 1].name == 'assign':
                    skipping_level = 1
                    skipping_checks = True
                    skipping_level_increase_token = 'leftbrace'
                    skipping_level_decrease_token = 'rightbrace'
                    continue

            if skipping_checks:
                if token.name == skipping_level_increase_token:
                    skipping_level += 1
                elif token.name == skipping_level_decrease_token:
                    skipping_level -= 1
                if skipping_level == 0:
                    skipping_checks = False
                continue
            if token.name == 'do':
                do_while_braces_count.append(0)
            elif token.name == 'enum':
                enum_braces_count.append(0)
            elif token.name == 'assign':
                assign_braces_count.append(0)
            elif token.name == 'union':
                union_braces_count.append(0)
            elif token.name == 'typedef' and i + 1 < tokens_count and tokens[i + 1].name == 'struct':
                typedef_struct_braces_count.append(0)
            elif token.name == 'struct':
                struct_braces_count.append(0)

            elif token.name == 'leftbrace':
                # Count the braces of a typedef struct, do_while and enum in order to detect the end of the bloc
                if len(do_while_braces_count) > 0:
                    do_while_braces_count[-1] += 1
                if len(enum_braces_count) > 0:
                    enum_braces_count[-1] += 1
                if len(assign_braces_count) > 0:
                    assign_braces_count[-1] += 1
                if len(union_braces_count) > 0:
                    union_braces_count[-1] += 1
                if len(typedef_struct_braces_count) > 0:
                    typedef_struct_braces_count[-1] += 1
                if len(struct_braces_count) > 0:
                    struct_braces_count[-1] += 1

                function = get_function_start_at_token(functions, token)
                if function is not None and len(lines[token.line - 1]) > 1:  # handling function specific case
                    abricot.report(file, token.line, "L4")
                elif function is None and i > 0 and tokens[i - 1].line != token.line:
                    abricot.report(file, token.line, "L4")

            elif token.name == 'rightbrace':
                # Count the braces of a typedef struct, do_while and enum in order to detect the end of the bloc
                if len(do_while_braces_count) > 0:
                    do_while_braces_count[-1] -= 1
                if len(enum_braces_count) > 0:
                    enum_braces_count[-1] -= 1
                if len(assign_braces_count) > 0:
                    assign_braces_count[-1] -= 1
                if len(union_braces_count) > 0:
                    union_braces_count[-1] -= 1
                if len(typedef_struct_braces_count) > 0:
                    typedef_struct_braces_count[-1] -= 1
                if len(struct_braces_count) > 0:
                    struct_braces_count[-1] -= 1

                # True when it's the end of the do_while bloc
                if len(do_while_braces_count) > 0 and do_while_braces_count[-1] == 0:
                    do_while_braces_count.pop()
                    continue

                # True when it's the end of the enum bloc
                if len(enum_braces_count) > 0 and enum_braces_count[-1] == 0:
                    enum_braces_count.pop()
                    continue

                # True when it's the end of the assign bloc
                if len(assign_braces_count) > 0 and assign_braces_count[-1] == 0:
                    assign_braces_count.pop()
                    continue

                # True when it's the end of the union bloc
                if len(union_braces_count) > 0 and union_braces_count[-1] == 0:
                    union_braces_count.pop()
                    continue

                # True when it's the end of the typedef struct bloc
                if len(typedef_struct_braces_count) > 0 and typedef_struct_braces_count[-1] == 0:
                    typedef_struct_braces_count.pop()
                    continue

                # True when it's the end of the struct bloc
                if len(struct_braces_count) > 0 and struct_braces_count[-1] == 0:
                    struct_braces_count.pop()
                    continue

                if i + 1 < tokens_count and tokens[i + 1].name == 'else':
                    continue
                line = token_line_content.replace(' ', '').replace('\t', '')
                is_valid = re.match("}[ \t]*;?(//.*|/\\*.*)?", line)
                if not is_valid:
                    abricot.report(file, token.line, "L4")
            elif token.name == 'else':
                # A righbrace preceding an else must be on the same line
                if i >= 1 and tokens[i - 1].name == 'rightbrace' and tokens[i - 1].line != token.line:
                    abricot.report(file, token.line, "L4")
                # Check if there is a valid token after the else on the same line
                if (
                        i + 1 >= tokens_count or
                        (tokens[i + 1].name not in ['if', 'leftbrace'] and tokens[i + 1].line == token.line)
                ):
                    abricot.report(file, token.line, "L4")

            elif token.name == 'if' and i >= 1 and tokens[i - 1].name == 'else':
                if token.line != tokens[i - 1].line:
                    abricot.report(file, token.line, "L4")




