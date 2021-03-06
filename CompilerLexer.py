from sly import Lexer
from CompilerException import CompilerException


# noinspection PyUnresolvedReferences,PyUnboundLocalVariable
class CompilerLexer(Lexer):
    tokens = {VAR, BEGIN, END,
              ASSIGN,
              IF, THEN, ELSE, ENDIF,
              WHILE, DO, ENDWHILE,
              REPEAT, UNTIL,
              FOR, FROM, TO, DOWNTO, ENDFOR,
              READ, WRITE,
              PLUS, MINUS, TIMES, DIV, MOD,
              EQ, NEQ, LE, GE, LEQ, GEQ,
              NUM, PIDENTIFIER}
    literals = {'[', ']', ':', ';', ','}  # - unary minus

    ignore = ' \t'

    @_(r'\([^\)]*\)')
    def ignore_comments(self, t):
        self.lineno += t.value.count('\n')

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    ENDWHILE = r'ENDWHILE'
    ASSIGN = r'ASSIGN'
    REPEAT = r'REPEAT'
    DOWNTO = r'DOWNTO'
    ENDFOR = r'ENDFOR'
    BEGIN = r'BEGIN'
    ENDIF = r'ENDIF'
    WHILE = r'WHILE'
    UNTIL = r'UNTIL'
    WRITE = r'WRITE'
    MINUS = r'MINUS'
    TIMES = r'TIMES'
    THEN = r'THEN'
    ELSE = r'ELSE'
    FROM = r'FROM'
    READ = r'READ'
    PLUS = r'PLUS'
    VAR = r'VAR'
    END = r'END'
    FOR = r'FOR'
    DIV = r'DIV'
    MOD = r'MOD'
    NEQ = r'NEQ'
    LEQ = r'LEQ'
    GEQ = r'GEQ'
    IF = r'IF'
    DO = r'DO'
    TO = r'TO'
    EQ = r'EQ'
    LE = r'LE'
    GE = r'GE'

    PIDENTIFIER = r'[_a-z]+'

    @_(r'-?\d+')
    def NUM(self, t):
        if t.value[0] == "-":
            t.value = -1 * int(t.value[1:])
        else:
            t.value = int(t.value)
        return t

    def error(self, t):
        raise CompilerException(f"Illegal character {t.value[0]}", self.lineno - 1)