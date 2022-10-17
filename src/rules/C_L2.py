import abricot

from utils import is_header_file, is_source_file, is_line_correctly_indented, get_lines


def checker(config):
    for file in abricot.getSourceFileNames(config):
        if not is_source_file(file) and not is_header_file(file):
            continue
        for line_number, line in enumerate(get_lines(file, replace_comments=True), start=1):
            if not is_line_correctly_indented(line):
                abricot.report(file, line_number, 'L2')



