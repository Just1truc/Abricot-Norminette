import re
from os import path
from sys import stderr
from typing import List

import abricot

LOWER_SNAKECASE_REGEX = re.compile(r'^[a-z](?:_?[a-z0-9]+)*$')
UPPER_SNAKECASE_REGEX = re.compile(r'^[A-Z](?:_?[A-Z0-9]+)*$')

BINARY_OPERATORS_TOKENS = [
    'plus',
    'minus',
    'star',
    'divide',
    'greater',
    'greaterequal',
    'less',
    'lessequal',
    'equal',
    'notequal',
    'orassign',
    'or',
    'andand',
    'and',
    'andassign',
    'percentassign',
    'percent',
    'plusassign',
    'minusassign',
    'shiftleftassign',
    'shiftrightassign',
    'divideassign',
    'starassign',
    'xor',
    'shiftleft',
    'shiftright',
    'xorassign',
    'assign',
    'signed',
    'oror',
    'colon',
    'question_mark'
]

PREPROCESSOR_TOKENS = [
    'pp_define',
    'pp_elif',
    'pp_else',
    'pp_endif',
    'pp_error',
    'pp_hheader',
    'pp_if',
    'pp_ifdef',
    'pp_ifndef',
    'pp_include',
    'pp_line',
    'pp_number',
    'pp_pragma',
    'pp_qheader',
    'pp_undef',
    'pp_warning'
]

UNARY_OPERATORS_TOKENS = [
    'and',
    'plus',
    'minus',
    'not',
    'sizeof',
    'star'
]

INCREMENT_DECREMENT_TOKENS = [
    'plusplus',
    'minusminus'
]

LITERALS_TOKENS = [
    'intlit',
    'stringlit',
    'charlit',
    'floatlit',
    'longintlit'
]

TYPES_TOKENS = [
    'auto',
    'bool',
    'char',
    'comma',
    'const',
    'decimalint',
    'double',
    'enum',
    'extern',
    'float',
    'hexaint',
    'inline',
    'int',
    'long',
    'mutable',
    'octalint',
    'register',
    'short',
    'signed',
    'static',
    'typedef',
    'union',
    'unsigned',
    'virtual',
    'void',
    'volatile',
    'struct'
]

IDENTIFIERS_TOKENS = [
    'identifier',
] + LITERALS_TOKENS

KEYWORDS_TOKENS = [
    'break',
    'default',
    'return',
    'case',
    'continue',
    'default',
    'goto',
    'typeid',
    'typename',
    'struct',
    'if',
    'for',
    'while',
    'do',
    'switch'
]

PARENTHESIS_TOKENS = [
    'leftparen',
    'rightparen'
]

SQUARE_BRACKETS_TOKENS = [
    'leftbracket',
    'rightbracket'
]


# pylint: disable=R0913
class Token:
    def __init__(self, file: str, value: str, line: int, column: int, name: str, type_: str):
        self.file = file
        self.value = value
        self.line = line
        self.column = column
        self.name = name
        self.type = type_


def is_header_file(file: str) -> bool:
    return file.endswith('.h') and not is_binary(file)


def is_source_file(file: str) -> bool:
    return file.endswith('.c') and not is_binary(file)


def is_makefile(file: str) -> bool:
    return get_filename(file).startswith("Makefile") and not is_binary(file)


def is_binary(file: str) -> bool:
    return abricot.isBinary(file)


def get_extension(file: str) -> str:
    _, extension = path.splitext(file)
    return extension


def get_filename_without_extension(file: str) -> str:
    extension = get_extension(file)
    if extension:
        return path.basename(path.splitext(file)[0])
    return path.basename(file)


def get_filename(file: str) -> str:
    return path.basename(file)


def is_upper_snakecase(raw: str) -> bool:
    return re.fullmatch(UPPER_SNAKECASE_REGEX, raw) is not None


def is_lower_snakecase(raw: str) -> str:
    return re.fullmatch(LOWER_SNAKECASE_REGEX, raw) is not None


def debug_print(s, **kwargs):
    print(s, file=stderr, flush=True, **kwargs)


def __remove_between(lines: List[str], token: Token, begin_token="//", end_token=None) -> None:
    for offset, value in enumerate(token.value.split("\n")):
        line = lines[token.line - 1 + offset]
        has_line_break = line.endswith('\\')

        head = line[:token.column] if offset == 0 else ""
        if (len(line) - (len(head) + len(value))) > 0:
            tail = line[-(len(line) - (len(head) + len(value))):]
        else:
            tail = ""

        if begin_token and end_token and value.startswith(begin_token) and value.endswith(end_token):
            line = head + begin_token + ' ' * (len(value) - (len(begin_token) + len(end_token))) + end_token + tail
        elif begin_token and value.startswith(begin_token):
            line = head + begin_token + ' ' * (len(value) - len(begin_token)) + tail
        elif end_token and value.endswith(end_token):
            line = head + ' ' * (len(value) - len(end_token)) + end_token + tail
        else:
            line = ' ' * len(line)

        if has_line_break:
            line = line[:-1] + '\\'

        lines[token.line - 1 + offset] = line


def __reset_token_value(lines: List[str], token:Token) -> Token:
    value = token.value
    line = lines[token.line - 1][token.column:]
    offset = 0
    while not line.replace('\\', '').replace('\n', '').startswith(value.replace('\\', '').replace('\n', '')) and (token.line - 1 + offset + 1) < len(lines):
        offset += 1
        line = line + '\n' + lines[token.line - 1 + offset]
    diff = len(line.replace('\\', '').replace('\n', '')) - len(value.replace('\\', '').replace('\n', ''))
    if diff > 0:
        line = line[:-diff]
    return Token(
        token.file,
        line,
        token.line,
        token.column,
        token.name,
        token.type)


def get_lines(file: str, replace_comments=False, replace_stringlits=False) -> List[str]:
    lines = abricot.getAllLines(file)
    if replace_comments or replace_stringlits:
        lines = [l[:] for l in lines]
    if replace_comments:
        comments = abricot.getTokens(file, 1, 0, -1, -1, ['ccomment', 'cppcomment'])
        for comment in comments:
            comment = __reset_token_value(lines, comment)
            if comment.type == 'ccomment':  # /*  */
                __remove_between(lines, comment, '/*', '*/')
            elif comment.type == 'cppcomment':  # //
                __remove_between(lines, comment, '//')

    if replace_stringlits:
        stringlits = abricot.getTokens(file, 1, 0, -1, -1, ['stringlit'])
        for stringlit in stringlits:
            stringlit = __reset_token_value(lines, stringlit)
            __remove_between(lines, stringlit, '"', '"')
    return lines


def is_line_empty(line: str):
    # A line only made of spaces is considered empty
    return len(line) == 0 or line.isspace()


def is_line_correctly_indented(line: str) -> bool:
    # A well-indented line is considered to either be:
    # - an empty line;
    # - a line only comprised of spaces (which should not be considered a violation of the L2 rule,
    #   but a violation of the C-G7 rule);
    # - a line with any amount of 4 spaces groups (can be 0, notably for top-level statements),
    #   followed by a non-space and non-tabulation character.
    # - a line part of a comment block
    if is_line_empty(line):
        return True
    indentation_regex = re.compile(r'^( *|( {4})*\S+.*)$')
    return indentation_regex.match(line.removesuffix('*/')) is not None


def get_index_from_raw(raw: str, line: int, column: int):
    lines = raw.split('\n')
    len_before_current_line = len('\n'.join(lines[:line - 1]))
    len_before_column = lines[line - 1][:column]
    return len_before_current_line + len_before_column


def get_prev_token_index(tokens: List[Token], index: int, types_filters: List[str]):
    for i in range(0, index):
        token = tokens[index - i - 1]
        if token.name in types_filters:
            return index - i - 1
    return -1


def get_next_token_index(tokens: List[Token], index: int, types_filters: List[str]):
    for i in range(index + 1, len(tokens)):
        token = tokens[i]
        if token.name in types_filters:
            return i
    return -1


def is_token_pointer(tokens: List[Token], index: int):
    token = tokens[index]
    prev_non_identifier_index = get_prev_token_index(tokens, index, TYPES_TOKENS + BINARY_OPERATORS_TOKENS + ['leftparen'])
    prev_identifier_index = get_prev_token_index(tokens, index, IDENTIFIERS_TOKENS)
    return token.name == 'star' and (
            prev_non_identifier_index > prev_identifier_index or
            prev_non_identifier_index < 0
    )
