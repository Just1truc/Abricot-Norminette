import abricot
from utils import get_lines
from utils import is_header_file, is_source_file, is_makefile

TAB_MAX_LENGTH = 4
LINE_MAX_LENGTH = 80


def checker(config):
    for file in abricot.getSourceFileNames():
        if not is_source_file(file) and not is_header_file(file) and not is_makefile(file):
            continue

        for line_number, line in enumerate(get_lines(file), start=1):
            count = 0
            for character in line:
                if character == '\t':
                    count = (count + TAB_MAX_LENGTH) - (count % TAB_MAX_LENGTH)
                else:
                    count += 1
            if count > LINE_MAX_LENGTH:
                abricot.report(file, line_number, "F3")



