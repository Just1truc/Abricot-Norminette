import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", default=None, nargs="?", help="File or directory to check")
parser.add_argument("--all", help="Report all coding style violations", action="store_true")
parser.add_argument("--format", help="Choose a format for the report", choices=["default", "json", "csv", "plain"], default="default")
parser.add_argument("--update", help="Update Abricot to the latest version", action="store_true")
parser.add_argument("--version", help="Display the current version of Abricot", action="store_true")
parser.add_argument("--group", help="Group errors by file or type", choices=["file", "type"], default="file")
parser.add_argument("--ignore", help="Use .gitignore configuration to detect files to ignore", action="store_true")
parser.add_argument("--status", help="Exit status of the program indicates if mistakes were found", action="store_true")
parser.add_argument("--nofunc", help="Don't report banned functions", action="store_true")