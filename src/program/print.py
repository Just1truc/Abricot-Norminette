from enum import Enum

class Colors(Enum):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BLACK = '\033[98m'
    GREY = '\033[90m'
    RESET = '\033[0m'

def printc(text: str, color: Colors = Colors.WHITE, bold: bool = False, end: str = "\n") -> None:
    print(("\033[1m" if bold else "") + color.value + text + Colors.RESET.value, end=end)