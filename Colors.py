class Colors:
    """
    A class to represent ANSI color codes for console outputs. This class provides
    various attributes for standard colors and custom pastel shades, which can be used
    to change the color of text output in terminal or command prompt.
    """
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    PASTEL_GREEN = '\033[38;2;119;221;119m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[0;35m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    PASTEL_PEACH = '\033[38;2;255;229;180m'
    PASTEL_BLUE = '\033[38;2;179;205;224m'
    PASTEL_ORANGE = '\033[38;2;255;179;71m'
