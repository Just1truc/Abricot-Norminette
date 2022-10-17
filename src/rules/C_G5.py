import re

import abricot
from utils import is_source_file, is_header_file


def checker(config):
    regex = r"^\s*#include\s*(?:<|\")(.*)(?:>|\")"
    for file in abricot.getSourceFileNames():
        if not is_source_file(file) and not is_header_file(file):
            continue
        for token in abricot.getTokens(file, 1, 0, -1, -1, ["pp_qheader"]):
            matches = re.finditer(regex, token.value, re.MULTILINE)
            for match in matches:
                for group_num in range(0, len(match.groups())):
                    group_num = group_num + 1
                    if not match.group(group_num).endswith(".h"):
                        abricot.report(file, token.line, "G5")



