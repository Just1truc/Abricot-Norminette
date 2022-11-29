from enum import Enum
import rules


class Severities(Enum):
    INFO = 1
    MINOR = 2
    MAJOR = 3


class Rule:
    def __init__(self, code: str, name: str, severity: Severities, description: str, checker: callable, optional: bool):
        self.code = code
        self.name = name
        self.severity = severity
        self.description = description
        self.checker = checker
        self.optional = optional


rules = {
    "A3": Rule("C-A3", "Line break at the end of file", Severities.INFO, "Files must end with a line break", rules.C_A3.checker, False),
    "C1": Rule("C-C1", "Conditonal branching", Severities.MAJOR, "A conditionnal block must not contain more than 3 branches", rules.C_C1.checker, False),
    "C2": Rule("C-C3", "Ternary operators", Severities.MAJOR, "The use of ternary operators is allowed as far as it is kept simple and readable", rules.C_C2.checker, True),
    "C3": Rule("C-C3", "Goto", Severities.MAJOR, "Oh no, cringe...", rules.C_C3.checker, False),
    "F2": Rule("C-F2", "Naming functions", Severities.MINOR, "Your function name is not enough explicit", rules.C_F2.checker, False),
    "F3": Rule("C-F3", "Number of columns", Severities.MAJOR, "The length of a line must not exceed 80 columns", rules.C_F3.checker, False),
    "F4": Rule("C-F4", "Number of lines", Severities.MAJOR, "The body of a function must not exceed 20 lines", rules.C_F4.checker, False),
    "F5": Rule("C-F5", "Number of parameters", Severities.MAJOR, "A function must not have more than 4 parameters", rules.C_F5.checker, False),
    "F6": Rule("C-F6", "Functions without parameters", Severities.MAJOR, "A function taking no parameters must take void as a parameter", rules.C_F6.checker, False),
    "F8": Rule("C-F8", "Comments inside a function", Severities.MINOR, "There must be no comment within a function", rules.C_F8.checker, False),
    "F9": Rule("C-F9", "Nested functions", Severities.MAJOR, "Nested functions are not allowed", rules.C_F9.checker, False),
    "G1": Rule("C-G1", "File header", Severities.MINOR, "Files must always start with the standard header", rules.C_G1.checker, False),
    "G2": Rule("C-G2", "Separation of functions", Severities.MINOR, "Implementations of functions must be separated by one empty line", rules.C_G2.checker, False),
    "G3": Rule("C-G3", "Indentation of preprocessor", Severities.MINOR, "The preprocessor directives must be indented", rules.C_G3.checker, False),
    "G4": Rule("C-G4", "Global variables", Severities.MAJOR, "Only global constants should be used", rules.C_G4.checker, False),
    "G5": Rule("C-G5", "Include", Severities.MAJOR, "Include directive must only include C header", rules.C_G5.checker, False),
    "G6": Rule("C-G6", "Line endings", Severities.MINOR, "Line endings must be done in UNIX style", rules.C_G6.checker, False),
    "G7": Rule("C-G7", "Trailing spaced", Severities.MINOR, "No trailing spaces must be present at the end of a line", rules.C_G7.checker, False),
    "G8": Rule("C-G8", "Leading/Trailing lines", Severities.MINOR, "No empty lines must be present", rules.C_G8.checker, False),
    "L1": Rule("C-L1", "Code line content", Severities.MINOR, "A line must correspond to only one statement", rules.C_L1.checker, True),
    "L2": Rule("C-L2", "Indentation", Severities.MINOR, "No tabulations may be used for indentation", rules.C_L2.checker, False),
    "L3": Rule("C-L3", "Spaces", Severities.MINOR, "You have misplaced space(s)", rules.C_L3.checker, False),
    "L4": Rule("C-L4", "Curly Brackets", Severities.MINOR, "You have misplaced curly bracket(s)", rules.C_L4.checker, False),
    "L5": Rule("C-L5", "Variable Declarations", Severities.MAJOR, "Variables must be declared one by one at the beginning of the scope of the function", rules.C_L5.checker, True),
    "O1": Rule("C-O1", "Contents of the repository", Severities.MAJOR, "The repository must not contain compiled, temporary or unnecessary files", rules.C_O1.checker, False),
    "O3": Rule("C-O3", "File coherence", Severities.MAJOR, "Your files can contain at most 5 functions", rules.C_O3.checker, False),
    "O4": Rule("C-O4", "Naming files and folders", Severities.MINOR, "Your files should be correctly named", rules.C_O4.checker, False),
    "V1": Rule("C-V1", "Naming identifiers", Severities.MINOR, "Your identifiers should be correctly named", rules.C_V1.checker, False),
    "FN": Rule("C-FN", "Banned function", Severities.MAJOR, "This syscall is usually banned in projects", rules.C_FN.checker, False),
}
