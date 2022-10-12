#!/usr/bin/python3

from program.abriThread import Abrifast
from program.profile import rules
from abricot import getAllErrors
from program.arguments import parser
from program.output import OutputManager
from program.ignored import getIgnoredFiles
from program.configuration import Configuration

args = parser.parse_args()
thread = Abrifast()

config = Configuration()

if args.update:
    from program.updater import update
    update()
    
if args.version:
    from __init__ import showVersion
    showVersion()

if args.ignore:
    config.ignored = getIgnoredFiles()
    
for rule in rules.values():
    thread.add(rule.checker, config, rule.name)

thread.run()

errors = getAllErrors()
output = OutputManager(errors)
output.groupBy(args.group)
output.showAs(args.format)