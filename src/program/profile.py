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
    "Ld": Rule("C-L3a", "Spaces", Severities.MINOR, "You have misplaced space(s)", rules.C_L3.checker),
    "Lr": Rule("C-L3z", "Spaces", Severities.MINOR, "You have misplaced space(s)", rules.C_L3.checker),
    "Le": Rule("C-L3e", "Spaces", Severities.MINOR, "You have misplaced space(s)", rules.C_L3.checker),
    "Ln": Rule("C-L3r", "Spaces", Severities.MINOR, "You have misplaced space(s)", rules.C_L3.checker),
    "Lb": Rule("C-L3t", "Spaces", Severities.MINOR, "You have misplaced space(s)", rules.C_L3.checker),
    "Lv": Rule("C-L3y", "Spaces", Severities.MINOR, "You have misplaced space(s)", rules.C_L3.checker),
    "Lc": Rule("C-L3u", "Spaces", Severities.MINOR, "You have misplaced space(s)", rules.C_L3.checker),
    "Lx": Rule("C-L3i", "Spaces", Severities.MINOR, "You have misplaced space(s)", rules.C_L3.checker),
    "Lw": Rule("C-L3o", "Spaces", Severities.MINOR, "You have misplaced space(s)", rules.C_L3.checker),
    "L3-": Rule("C-Lk3", "Spaces", Severities.MINOR, "You have misplaced space(s)", rules.C_L3.checker),
    "L3)": Rule("C-L3k", "Spaces", Severities.MINOR, "You have misplaced space(s)", rules.C_L3.checker),
}
