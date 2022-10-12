import os
import subprocess
import abricot
from program.print import printc, Colors
from utils import is_source_file, is_header_file
from program.configuration import Configuration

CLANG_CONFIG = "AlignAfterOpenBracket: false\nAlignArrayOfStructures: None\nAlignConsecutiveMacros: None\nAlignConsecutiveAssignments: None\nAlignConsecutiveBitFields: None\nAlignConsecutiveDeclarations: None\nAlignEscapedNewlines: Right\nAlignOperands: false\nAlignTrailingComments: false\nAllowAllArgumentsOnNextLine: true\nAllowAllParametersOfDeclarationOnNextLine: true\nAllowShortEnumsOnASingleLine: true\nAllowShortBlocksOnASingleLine: Never\nAllowShortCaseLabelsOnASingleLine: false\nAllowShortFunctionsOnASingleLine: All\nAllowShortLambdasOnASingleLine: All\nAllowShortIfStatementsOnASingleLine: true\nAllowShortLoopsOnASingleLine: false\nAlwaysBreakAfterDefinitionReturnType: None\nAlwaysBreakAfterReturnType: None\nAlwaysBreakBeforeMultilineStrings: false\nAlwaysBreakTemplateDeclarations: MultiLine\nAllowAllConstructorInitializersOnNextLine: true\nFixNamespaceComments: false\nColumnLimit: 0\nIndentWidth: 4\nKeepEmptyLinesAtTheStartOfBlocks: true\nMaxEmptyLinesToKeep: 9999999\nNamespaceIndentation: None\nBreakBeforeBraces: Custom"

def getFormatedFile(file, original):
    try:
        p = subprocess.Popen(["clang-format", file], stdout=subprocess.PIPE)
        result = p.communicate()[0].decode("utf-8")
        return replaceLinebreaks(original, result)
    except FileNotFoundError:
        return None

def getFileContent(file):
    with open(file, "r") as f:
        return f.read()

def replaceLinebreaks(original, formated):
    original = original.replace(" ", "").replace("\t", "")
    linebreaks = [i for i, c in enumerate(original) if c == "\n"]
    formated = formated.replace("\n", "")
    index_without_spaces = 0
    len_linebreaks = len(linebreaks)
    len_formated = len(formated)
    result = ""
    for i in range(len_formated):
        while len_linebreaks > 0 and index_without_spaces == linebreaks[0]:
            result += "\n"
            linebreaks.pop(0)
            len_linebreaks -= 1
            index_without_spaces += 1
        result += formated[i]
        if formated[i] != " " and formated[i] != "\t":
            index_without_spaces += 1   
    return result

def getMisplacedSpaces(file, original, formated):
    original_lines = original.splitlines()
    formated_lines = formated.splitlines()
    n_formated = len(formated_lines)
    for i, line in enumerate(original_lines):
        if i >= n_formated:
            break
        trimmed_line = line.strip()
        trimmed_formated = formated_lines[i].strip()
        if trimmed_line != trimmed_formated and trimmed_line.replace(" ", "") == trimmed_formated.replace(" ", ""):
            abricot.report(file, i + 1, "L3")

def checker(config: Configuration):
    if os.path.exists(".clang-format"):
        os.rename(".clang-format", ".clang-format.bak")
    with open(".clang-format", "w") as f:
        f.write(CLANG_CONFIG)
    for file in abricot.getSourceFileNames(config):
        if not is_source_file(file) and not is_header_file(file):
            continue
        original = getFileContent(file)
        formated = getFormatedFile(file, original)
        if formated is None:
            printc("[WARNING] We detected a problem with clang-format. C-L3 won't be checked", bold=True, color=Colors.YELLOW)
            print("  ↪ To fix it please try installing clang-format with your package manager.", end="\n\n")
            break
        getMisplacedSpaces(file, original, formated)
    os.remove(".clang-format")
    if os.path.exists(".clang-format.bak"):
        os.rename(".clang-format.bak", ".clang-format")