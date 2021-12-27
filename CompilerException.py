class CompilerException(Exception):
    def __init__(self, lineno, reason):
        message = f"Error in line {lineno}: {reason}"
        super().__init__(message)
