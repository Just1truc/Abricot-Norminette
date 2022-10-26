import re

ATTRIBUTE_REGEX = re.compile(r"__attribute__\(\(\w*\)\)")

def get_column(raw: str, line_number: int, index: int):
    if line_number == 1:
        last_newline_index = 0
    else:
        last_newline_index = raw[:index].rindex('\n') + 1
    return index - last_newline_index

def remove_attributes(raw: str, keep_char_count: bool = True):
    matches = re.finditer(ATTRIBUTE_REGEX, raw)
    offset = 0

    for match in matches:
        match_size = match.end() - match.start()
        char_count = match_size * keep_char_count
        offset += match_size * (not keep_char_count)
        start = match.start() - offset
        end = match.end() - offset
        raw = raw[:start] + (' ' * char_count) + raw[end:]
    return raw
