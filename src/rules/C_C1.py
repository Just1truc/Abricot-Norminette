from dataclasses import dataclass
from enum import Enum
from typing import List

import abricot
from utils import is_source_file, is_header_file
from utils.functions import get_functions

# The maximum depth of nested control structures allowed before reporting a violation
MAX_DEPTH_ALLOWED = 2


class _State(Enum):
    NOTHING = 0
    CONDITIONAL = 1
    ELSEIF = 2
    ELSE = 3


@dataclass
class ControlStructure:
    type: str
    has_braces: bool


# pylint:disable=too-many-nested-blocks
# pylint:disable=too-many-branches
# pylint:disable=too-many-statements
def _check_for_function(file, tokens):
    """
    :param file: The file currently being checked
    :param tokens: The tokens of the function being checked
    """

    # The index of the current token
    index = 0

    # The current control structure type the check is being conducted in
    state: _State = _State.NOTHING

    # The depth of nested control structures (0 at first, 1 with an if, 2 with a while in an if, etc.)
    depth = 0

    # The amount of currently unclosed opening parentheses encountered
    parenthesis_nesting_level = 0

    # The current stack of control structures
    control_structures_stack: List[ControlStructure] = []

    while index < len(tokens):
        token = tokens[index]
        token_type = token.type
        token_line = token.line
        # If a "{" is encountered as part of a control structure,
        # it increases the structure nesting level by 1
        # and sets the fact that further parentheses are not that of the keyword
        if token_type == 'leftbrace':
            index += 1
            if state != _State.NOTHING and len(control_structures_stack) > 0:
                control_structures_stack[-1].has_braces = True
        # If a "}" is encountered as part of a control structure,
        # it decreases the structure nesting level and the depth by 1
        elif token_type == 'rightbrace':
            if state != _State.NOTHING:
                depth -= 1
                if len(control_structures_stack) > 0:
                    control_structures_stack.pop(-1)
                while len(control_structures_stack) > 0 and not control_structures_stack[-1].has_braces:
                    control_structures_stack.pop(-1)
                    depth -= 1
            index += 1
        # If an ";" is encountered after the parentheses of a keyword that does not have braces,
        # it considers the control structure "closed" and decreases the depth of all nested braceless structures
        elif token_type == 'semicolon':
            if parenthesis_nesting_level == 0 and state != _State.NOTHING:
                while len(control_structures_stack) > 0 and not control_structures_stack[-1].has_braces:
                    next_index = index + 1
                    next_token = None
                    while next_index < len(tokens) and next_token is None:
                        if tokens[next_index].type != 'newline':
                            next_token = tokens[next_index]
                        next_index += 1
                    next_token_type = next_token.type if next_token else None
                    depth -= 1
                    last_stacked_control_structure = control_structures_stack.pop(-1)
                    if last_stacked_control_structure.type == 'if' and next_token_type == 'else':
                        break
            index += 1
        elif token_type == 'else':
            next_token = tokens[index + 1]
            next_token_type = next_token.type
            depth += 1
            if next_token_type == 'if':
                depth += 1
                control_structures_stack.append(ControlStructure('else', False))
                control_structures_stack.append(ControlStructure('if', False))
                if state != _State.ELSEIF:
                    state = _State.ELSEIF
                    if depth > MAX_DEPTH_ALLOWED:
                        abricot.report(file, token_line, 'C1')
                else:
                    # Two consecutive "else if" statements
                    abricot.report(file, next_token.line, 'C1')
                index += 1
            else:
                control_structures_stack.append(ControlStructure('else', False))
                state = _State.ELSE
            index += 1
        elif token_type in ['if', 'while', 'for']:
            depth += 1
            control_structures_stack.append(ControlStructure(token_type, False))
            if depth > MAX_DEPTH_ALLOWED:
                abricot.report(file, token_line, 'C1')
            state = _State.CONDITIONAL
            index += 1
        elif token_type == 'newline' and depth == 0 and state != _State.NOTHING:
            next_token = tokens[index + 1] if index + 1 < len(tokens) else None
            next_token_type = next_token.type if next_token else None
            next_token_line = next_token.line if next_token else None
            if next_token is None or not (next_token_type == 'else' and next_token_line == token_line + 1):
                state = _State.NOTHING
            index += 1
        else:
            if state != _State.NOTHING:
                if token_type == 'leftparen':
                    parenthesis_nesting_level += 1
                elif token_type == 'rightparen':
                    parenthesis_nesting_level -= 1
            index += 1


def checker(config):
    for file in abricot.getSourceFileNames():
        if not (is_source_file(file) or is_header_file(file)):
            continue

        for func in get_functions(file):
            if func.body is not None:
                tokens = abricot.getTokens(file,
                                        func.body.line_start, func.body.column_start,
                                        func.body.line_end, func.body.column_end,
                                        ['if', 'else', 'while', 'for',
                                         'semicolon',
                                         'leftbrace', 'rightbrace',
                                         'newline',
                                         'leftparen', 'rightparen'])
                _check_for_function(file, tokens)



