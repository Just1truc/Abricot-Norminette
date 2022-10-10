import abricot
import re
from .function import Function
from .section import Section
from .utils import remove_attributes, get_column
from utils import get_lines
from typing import List

RESERVED_KEYWORDS = [
    "break",
    "case",
    "continue",
    "default",
    "do",
    "else",
    "extern",
    "for",
    "goto",
    "if",
    "return",
    "sizeof",
    "switch",
    "typedef",
    "while"
]

FUNCTION_REGEX = re.compile(
    r"(?P<beforeFunction>(^|#.+|(?<=[;}{]))([\n\s*/]*(^|(?<=[\n\s{};]))))"
    r"(?P<func>"
    r"(?P<type>((?!" + r"\W|".join(RESERVED_KEYWORDS) + r"\W)\w+[\w\s\n*,]*|(\w+[\s\t\n*]+)\(\*.*\)\(.*\))[\s\n*]+)"
    r"(?P<name>(?<=[\n\s*])\w+)[\s\n]*\([\n\s]*"
    r"(?P<args>[^;{]*)[\n\s]*\)[\s\n]*"
    r"(?P<functionStartChar>[;{]{1}))"
)

def __get_function_body(file: str, function_start_index: int):
    all_lines = get_lines(file, replace_comments=True)
    raw = '\n'.join(all_lines)
    braces_count = 0
    line_number = raw[:function_start_index].count('\n') + 1
    column_number = get_column(raw, line_number, function_start_index)
    tokens = abricot.getTokens(file, line_number, column_number, -1, -1, ['leftbrace', 'rightbrace'])
    end_line_number = -1
    end_column_number = -1

    for token in tokens:
        if token.name == 'leftbrace':
            if braces_count == 0:
                line_number = token.line
                column_number = token.column
            braces_count += 1
        elif token.name == 'rightbrace':
            braces_count -= 1
        if braces_count == 0:
            end_line_number = token.line
            end_column_number = token.column
            break
    function_lines = all_lines[line_number - 1:end_line_number]
    function_lines[0] = function_lines[0][column_number:]
    function_lines[-1] = function_lines[-1][:end_column_number+1]
    raw = '\n'.join(function_lines)
    return Section(
        start = function_start_index,
        end = function_start_index + len(raw),
        line_start = line_number,
        line_end = end_line_number,
        column_start = column_number,
        column_end = end_column_number,
        raw = raw
    )

def __get_arguments_from_string(arguments_string: str):
    arguments_parts_array = arguments_string.split(',')
    argument = ""
    count = 0
    arguments = []

    for argument_part in arguments_parts_array:
        argument += argument_part
        if len(argument.strip()) > 0 and argument.count('(') == argument.count(')'):
            count += 1
            arguments.append(argument)
            argument = ""
    return arguments

def get_functions(file: str) -> List[Function]:
    raw = '\n'.join(get_lines(file, replace_comments=True, replace_stringlits=True))
    uncommented = remove_attributes(raw)
    matches = re.finditer(FUNCTION_REGEX, uncommented)
    functions = []
    for match in matches:
        before_function_len = len(match.group("beforeFunction"))
        match_start = match.start() + before_function_len + 1
        raw_match = match.group()[before_function_len + 1:]
        if match.group("functionStartChar") == ';':
            function_body = None
        else:
            function_body = __get_function_body(file, match.end() - 1)
        proto_start_line = raw.count('\n', 0, match.start()) + match.group("beforeFunction").count('\n') + 1
        proto_start_column = get_column(raw, proto_start_line, match_start - 1)
        proto_end_line = proto_start_line + raw_match.count('\n')
        proto_end_column = get_column(raw, proto_end_line, match.end() - 1)
        prototype_raw = raw_match[:match.end() - 1]
        functions.append(Function(
            prototype = Section(
                start = match_start,
                end = match.end() - 1,
                line_start = proto_start_line,
                line_end = proto_end_line,
                column_start = proto_start_column,
                column_end = proto_end_column,
                raw = prototype_raw
            ),
            body = function_body,
            raw = prototype_raw + (function_body.raw if function_body else ""),
            return_type = match.group("type"),
            name = match.group("name"),
            arguments = __get_arguments_from_string(match.group("args")),
        ))
    return functions
