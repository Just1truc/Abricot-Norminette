import abricot

from utils import is_header_file, is_source_file, is_makefile, get_lines


def checker(config):
    for file in abricot.getSourceFileNames(config):
        if not is_source_file(file) and not is_header_file(file) and not is_makefile(file):
            continue
        for line_number, line in enumerate(get_lines(file), start=1):
            if '\r' in line:
                abricot.report(file, line_number, "G6")


