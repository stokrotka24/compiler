import sys

from sly import Parser
from CompilerLexer import CompilerLexer
from CompilerException import CompilerException
from CodeGenerator import CodeGenerator
from SymbolTable import SymbolTable, Variable


# noinspection PyUnresolvedReferences
class CompilerParser(Parser):
    tokens = CompilerLexer.tokens
    symbol_table = SymbolTable()
    codeGenerator = CodeGenerator(symbol_table)

    @_('VAR declarations BEGIN commands END', 'BEGIN commands END')
    def program(self, p):
        asm = p.commands
        asm += "HALT"
        return asm

    @_('declarations "," PIDENTIFIER', 'PIDENTIFIER')
    def declarations(self, p):
        message = self.symbol_table.variable_declaration(p.PIDENTIFIER)
        if message:
            raise CompilerException(p.lineno, message)

    # @_('declarations "," PIDENTIFIER "[" NUM ":" NUM "]"')
    # def declarations(self, p):
    #     pass
    #
    # @_('PIDENTIFIER "[" NUM ":" NUM "]"')
    # def declarations(self, p):
    #     pass

    @_('commands command')
    def commands(self, p):
        return p.commands + p.command

    @_('command')
    def commands(self, p):
        return p.command

    @_('identifier ASSIGN expression ";"')
    def command(self, p):
        asm = ""
        asm += p.expression
        asm += "SWAP g\n"
        code, variable_name = p.identifier
        asm += code
        asm += "SWAP g\n"
        asm += "STORE g\n"
        self.symbol_table[variable_name].initialized = True
        return asm

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
        asm, variable_name = p.identifier
        asm += self.codeGenerator.store_variable_value(variable_name)
        return asm

    @_('WRITE value ";"')
    def command(self, p):
        asm, _, _ = p.value
        asm += "PUT\n"
        return asm

    @_('value')
    def expression(self, p):
        asm, _, _ = p.value
        return asm

    @_('value PLUS value')
    def expression(self, p):
        type0 = p.value0[1]
        type1 = p.value1[1]
        asm = ""
        if type0 == "constant" and type1 == "constant":
            num0 = p.value0[2]
            num1 = p.value1[2]
            asm += self.codeGenerator.generate_constant(num0+num1)
        else:
            asm += p.value0[0]
            asm += "SWAP g\n"
            asm += p.value1[0]
            asm += "ADD g\n"
        return asm

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
        return self.codeGenerator.generate_constant(p.NUM), "constant", p.NUM

    @_('identifier')
    def value(self, p):
        asm, variable_name = p.identifier
        try:
            asm += self.codeGenerator.load_variable_value(variable_name)
        except Exception as e:
            raise CompilerException("unknown", e)
        return asm, "variable", variable_name

    @_('PIDENTIFIER')
    def identifier(self, p):
        try:
            return self.codeGenerator.load_variable_address(p.PIDENTIFIER), p.PIDENTIFIER
        except Exception as e:
            raise CompilerException(p.lineno, e)

    # @_('PIDENTIFIER "[" PIDENTIFIER "]"')
    # def identifier(self, p):
    #     pass
    #
    # @_('PIDENTIFIER "[" NUM "]"')
    # def identifier(self, p):
    #     pass


if __name__ == '__main__':
    lexer = CompilerLexer()
    parser = CompilerParser()

    if len(sys.argv) != 3:
        raise Exception("usage: python3.8 CompilerParser.py <input_file> <output_file>")

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    with open(input_file) as f:
        text = f.read()
    tokenize_res = lexer.tokenize(text)
    # print("LEXER RESULT:")
    # for tok in tokenize_res:
    #     print(tok)
    # print("================")
    result = parser.parse(tokenize_res)
    print(parser.symbol_table)
    # print(result)
    with open(output_file, 'w') as f:
        f.write(result)
