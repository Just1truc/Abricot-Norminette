from enum import Enum
import rules


class Severities(Enum):
    INFO = 1
    MINOR = 2
    MAJOR = 3


class Rule:
    def __init__(self, code: str, name: str, severity: Severities, description: str, checker: callable):
        self.code = code
        self.name = name
        self.severity = severity
        self.description = description
        self.checker = checker


rules = {
    "L3": Rule("C-L3", "Spaces", Severities.MINOR, "You have misplaced space(s)", rules.C_L3.checker),
}
