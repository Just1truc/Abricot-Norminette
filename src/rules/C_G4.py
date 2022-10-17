import abricot

from utils import is_source_file, is_header_file


def acceptPairs(file, tokens, index=0, level=0, state="other"):
    end = len(tokens)
    while index != end:
        token = tokens[index]

        if token.type == "leftbrace":
            index += 1
            level += 1
            acceptPairs(file, tokens, index, level, state)
            if index == end:
                return

            index += 1
        elif token.type == "assign":
            index += 1
            if level == 0 and state != "const":
                state = "assign"
            elif level == 0:
                state = "constassign"

        elif token.type == "rightbrace":
            level -= 1
            if level == 0:
                state = "other"
            return
        elif token.type == "semicolon":
            index += 1
            if level == 0 and state == "assign":
                abricot.report(file, token.line, "G4")
            state = "other"
        elif token.type == "const":
            index += 1
            if level == 0 and state == "other":
                state = "const"

def checker(config):
    for file in abricot.getSourceFileNames(config):
        if not (is_source_file(file) or is_header_file(file)):
            continue
        tokens = abricot.getTokens(
            file, 1, 0, -1, -1, ["const", "semicolon", "assign", "leftbrace", "rightbrace"])
        acceptPairs(file, tokens)


