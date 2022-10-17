#!/usr/bin/python3

import os
from program.abriThread import Abrifast
from program.profile import rules
from abricot import getAllErrors, TokenizerObject, getSourceFileNames
from program.arguments import parser
from program.output import OutputManager
from program.ignored import getIgnoredFiles
from program.configuration import Configuration
from program.print import printc, Colors


args = parser.parse_args()
thread = Abrifast()

config = Configuration()


if args.file:
    if os.path.isdir(args.file):
        config.dir = args.file
    elif os.path.isfile(args.file):
        config.file = args.file
    else:
        printc("ERROR: File or directory '%s' not found" % args.file, bold=True, color=Colors.RED)
        exit(1)


if args.update:
    from program.updater import update
    update()
    
if args.version:
    from __init__ import showVersion
    showVersion()

if args.ignore:
    config.ignored = getIgnoredFiles()

TokenizerObject.setFiles(getSourceFileNames(config))

for rule in rules.values():
    if not rule.optional or args.all:
        thread.add(rule.checker, config, rule.name)

thread.run()

errors = getAllErrors()
output = OutputManager(errors)
output.groupBy(args.group)
output.showAs(args.format)

if args.status:
    exit(len(errors) > 0)