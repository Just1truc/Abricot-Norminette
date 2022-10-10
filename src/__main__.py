from profile import rules
from abricot import getAllErrors

for rule in rules.values():
    rule.checker()

errors = getAllErrors()
