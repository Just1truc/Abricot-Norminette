import re

import abricot
from utils import is_source_file, is_header_file, is_makefile, get_lines

MAKEFILE_HEADER_REGEX = re.compile(
    r'^##\n'
    r'## EPITECH PROJECT, [0-9]{4}\n'
    r'## \S.+\n'
    r'## File description:\n'
    r'(## .*\n)+'
    r'##(\n|$)')

C_HEADER_REGEX = re.compile(
    r'^/\*\n'
    r'\*\* EPITECH PROJECT, [0-9]{4}\n'
    r'\*\* \S.+\n'
    r'\*\* File description:\n'
    r'(\*\* .*\n)+'
    r'\*/(\n|$)')


def checker(config):
    for file in abricot.getSourceFileNames():
        if not is_source_file(file) and not is_header_file(file) and not is_makefile(file):
            continue
        raw = '\n'.join(get_lines(file))
        if (is_source_file(file) or is_header_file(file)) and not re.match(C_HEADER_REGEX, raw):
            abricot.report(file, 1, 'G1')
        if is_makefile(file) and not re.match(MAKEFILE_HEADER_REGEX, raw):
            abricot.report(file, 1, 'G1')



