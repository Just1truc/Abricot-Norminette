import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--all", help="Report all coding style violations", action="store_true")
parser.add_argument("--format", help="Choose a format for the report", choices=["default", "json", "csv", "plain"], default="default")
parser.add_argument("--update", help="Update Abricot to the latest version", action="store_true")
parser.add_argument("--version", help="Display the current version of Abricot", action="store_true")
