import abricot

from utils import is_header_file, is_source_file, is_makefile, get_lines, is_line_empty


def checker(config):
    for file in abricot.getSourceFileNames(config):
        if not is_source_file(file) and not is_header_file(file) and not is_makefile(file):
            continue

        file_lines = get_lines(file)

        # Empty files or files with only one line cannot have leading or trailing lines, regardless of their content
        if len(file_lines) < 2:
            continue

        # Leading lines
        lowest_line_checked = 0
        for line_number, line in enumerate(file_lines, start=1):
            lowest_line_checked = line_number
            if is_line_empty(line):
                abricot.report(file, line_number, "G8")
            else:
                break

        # Trailing lines
        # Prevents the lines reported as leading from being reported as trailing as well,
        # in the case of a file with only empty lines
        trailing_lines = []
        for i in range(len(file_lines) - 1, lowest_line_checked - 1, -1):
            line_number = i + 1
            line = file_lines[i]
            if is_line_empty(line):
                trailing_lines.insert(0, line_number)
            else:
                break
        for line_number in trailing_lines[1:]:
            abricot.report(file, line_number, "G8")



