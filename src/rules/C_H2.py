import re

import abricot
from utils import is_header_file, get_lines

PRAGMA_ONCE_REGEX = re.compile(r'\s*#\s*pragma\s+once\s*(//|/\*|$)')
IFNDEF_REGEX = re.compile(r'\s*#\s*ifndef\s+(?P<guard_name>\w+)\s*(//|/\*|$)')
DEFINE_REGEX = re.compile(r'\s*#\s*define\s+(?P<guard_name>\w+)\s*(//|/\*|$)')


def _is_protected_by_pragma_once(file):
    for pragma_token in abricot.getTokens(file, 1, 0, -1, -1, ['pp_pragma']):
        # pragma_token.value only returns 'pragma',
        # thus as a workaround we fetch all the line at which the directive is encountered.
        pragma_directive = get_lines(file)[pragma_token.line - 1]
        if PRAGMA_ONCE_REGEX.match(pragma_directive):
            return True
    return False


def _is_protected_by_ifndef(file):
    ifndef_token_list = abricot.getTokens(file, 1, 0, -1, -1, ['pp_ifndef'])
    define_token_list = abricot.getTokens(file, 1, 0, -1, -1, ['pp_define'])
    endif_token_list = abricot.getTokens(file, 1, 0, -1, -1, ['pp_endif'])

    if len(ifndef_token_list) > 0 and len(define_token_list) > 0 and len(endif_token_list) > 0:
        ifndef_token = get_lines(file)[ifndef_token_list[0].line - 1]
        match = IFNDEF_REGEX.match(ifndef_token)
        if match is None:
            return False
        guard_name = match.group('guard_name')
        define_token = get_lines(file)[define_token_list[0].line - 1]
        if guard_name:
            define_guard_match = DEFINE_REGEX.match(define_token)
            return define_guard_match and guard_name == define_guard_match.group('guard_name')
    return False


def checker(config):
    for file in abricot.getSourceFileNames():
        if not is_header_file(file):
            continue
        protected = _is_protected_by_ifndef(file) or _is_protected_by_pragma_once(file)

        if not protected:
            abricot.report(file, 1, "H2")



