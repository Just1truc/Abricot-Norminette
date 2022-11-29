import abricot
from utils import is_source_file
from utils.functions import get_functions
from utils import TYPES_TOKENS, PARENTHESIS_TOKENS


def check_structure_pointers():
    for file in abricot.getSourceFileNames():
        if not is_source_file(file):
            continue
        functions = get_functions(file)
        for function in functions:
            tokens = abricot.getTokens(file, function.prototype.line_start, function.prototype.column_start,
                                       function.prototype.line_end, function.prototype.column_end, ['identifier', 'star'] + TYPES_TOKENS + PARENTHESIS_TOKENS)
            params_tokens = []
            for token in tokens:
                if token.name == 'leftparen':
                    params_tokens.append([])
                    continue
                if len(params_tokens) == 0:
                    continue
                if token.name == 'rightparen':
                    break
                if token.name == 'comma':
                    params_tokens.append([])
                    continue
                params_tokens[-1].append(token)
            for param in params_tokens:
                if len(param) < 2:
                    continue
                if not any([tok.name == 'struct' for tok in param]):
                    continue
                for i in range(len(param) - 1):
                    if param[i].name == 'identifier' and param[i + 1].name == 'identifier':
                        abricot.report(file, param[i].line, 'F7')


def checker():
    check_structure_pointers()
