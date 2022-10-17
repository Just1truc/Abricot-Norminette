import abricot

from utils import is_source_file, is_header_file, is_makefile, get_lines


def checker(config):
    for file in abricot.getSourceFileNames():
        if not is_source_file(file) and not is_header_file(file) and not is_makefile(file):
            continue

        lines = get_lines(file)
        if lines[-1] != '':
            abricot.report(file, len(lines), 'A3')



