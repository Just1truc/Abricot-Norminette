#!/usr/bin/python3
from program.abriThread import Abrifast
from program.profile import rules
from abricot import getAllErrors
from program.arguments import parser
from program.output import OutputManager

args = parser.parse_args()
thread = Abrifast()
if args.update:
    from program.updater import update
    update()
    
if args.version:
    from __init__ import showVersion
    showVersion()

for rule in rules.values():
    thread.add(rule.checker, rule.name)

thread.run()

errors = getAllErrors()
output = OutputManager(errors)
output.groupBy(args.group)
output.showAs(args.format)