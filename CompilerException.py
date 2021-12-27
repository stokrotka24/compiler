class CompilerException(Exception):
    def __init__(self, reason, lineno='?'):
        message = f"Error in line {lineno}: {reason}"
        super().__init__(message)
