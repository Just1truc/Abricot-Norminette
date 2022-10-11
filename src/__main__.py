from program.profile import rules
from abricot import getAllErrors
from program.arguments import parser

args = parser.parse_args()

if args.update:
    from program.updater import update
    update()
    
if args.version:
    from __init__ import showVersion
    showVersion()

for rule in rules.values():
    rule.checker()

errors = getAllErrors()
