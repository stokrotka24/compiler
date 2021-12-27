from sly import Parser
from CompilerLexer import CompilerLexer


# noinspection PyUnresolvedReferences
class CompilerParser(Parser):
    tokens = CompilerLexer.tokens

    @_('VAR declarations BEGIN commands END')
    def program(self, p):
        return 2

    @_('BEGIN commands END')
    def program(self, p):
        pass

    @_('declarations "," PIDENTIFIER')
    def declarations(self, p):
        pass

    @_('declarations "," PIDENTIFIER "[" NUM ":" NUM "]"')
    def declarations(self, p):
        pass

    @_('PIDENTIFIER')
    def declarations(self, p):
        pass

    @_('PIDENTIFIER "[" NUM ":" NUM "]"')
    def declarations(self, p):
        pass

    @_('commands command')
    def commands(self, p):
        pass

    @_('command')
    def commands(self, p):
        pass

    # @_('identifier ASSIGN expression ";"')
    # def command(self, p):
    #     pass
    #
    # @_('IF condition THEN commands ELSE commands ENDIF')
    # def command(self, p):
    #     pass
    #
    # @_('IF condition THEN commands ENDIF')
    # def command(self, p):
    #     pass
    #
    # @_('WHILE condition DO commands ENDWHILE')
    # def command(self, p):
    #     pass
    #
    # @_('REPEAT commands UNTIL condition ";"')
    # def command(self, p):
    #     pass
    #
    # @_('FOR PIDENTIFIER FROM value TO value DO commands ENDFOR')
    # def command(self, p):
    #     pass
    #
    # @_('FOR PIDENTIFIER FROM value DOWNTO value DO commands ENDFOR')
    # def command(self, p):
    #     pass

    @_('READ identifier ";"')
    def command(self, p):
        pass

    @_('WRITE value ";"')
    def command(self, p):
        pass

    # @_('value')
    # def expression(self, p):
    #     pass
    #
    # @_('value PLUS value')
    # def expression(self, p):
    #     pass
    #
    # @_('value MINUS value')
    # def expression(self, p):
    #     pass
    #
    # @_('value TIMES value')
    # def expression(self, p):
    #     pass
    #
    # @_('value DIV value')
    # def expression(self, p):
    #     pass
    #
    # @_('value MOD value')
    # def expression(self, p):
    #     pass
    #
    # @_('value EQ value')
    # def condition(self, p):
    #     pass
    #
    # @_('value NEQ value')
    # def condition(self, p):
    #     pass
    #
    # @_('value LE value')
    # def condition(self, p):
    #     pass
    #
    # @_('value GE value')
    # def condition(self, p):
    #     pass
    #
    # @_('value LEQ value')
    # def condition(self, p):
    #     pass
    #
    # @_('value GEQ value')
    # def condition(self, p):
    #     pass

    @_('NUM')
    def value(self, p):
        pass

    @_('identifier')
    def value(self, p):
        pass

    @_('PIDENTIFIER')
    def identifier(self, p):
        pass

    @_('PIDENTIFIER "[" PIDENTIFIER "]"')
    def identifier(self, p):
        pass

    @_('PIDENTIFIER "[" NUM "]"')
    def identifier(self, p):
        pass


if __name__ == '__main__':
    lexer = CompilerLexer()
    parser = CompilerParser()

    with open("parser_tests/declaration.txt") as f:
        text = f.read()
    tokenize_res = lexer.tokenize(text)
    # print("LEXER RESULT:")
    # for tok in tokenize_res:
    #     print(tok)
    # print("================")
    result = parser.parse(tokenize_res)
    print(result)
