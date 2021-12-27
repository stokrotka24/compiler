import sys

from sly import Parser
from CompilerLexer import CompilerLexer
from CompilerException import CompilerException
from CodeGenerator import CodeGenerator
from SymbolTable import SymbolTable, Variable
from ParserAttrs import IdentifierAttr, ValueAttr


# noinspection PyUnresolvedReferences
class CompilerParser(Parser):
    tokens = CompilerLexer.tokens
    symbol_table = SymbolTable()
    code_generator = CodeGenerator(symbol_table)

    @_('VAR declarations BEGIN commands END', 'BEGIN commands END')
    def program(self, p):
        asm = p.commands
        asm.append("HALT")
        return asm

    @_('declarations "," PIDENTIFIER', 'PIDENTIFIER')
    def declarations(self, p):
        message = self.symbol_table.variable_declaration(p.PIDENTIFIER)
        if message:
            raise CompilerException(message, p.lineno)

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
        return self.code_generator.assign(p.identifier, p.expression)

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
        asm, var_name = p.identifier.var_address_asm, p.identifier.var_name
        asm += self.code_generator.store_variable_value(var_name)
        return asm

    @_('WRITE value ";"')
    def command(self, p):
        asm = p.value.get_value_asm
        asm.append("PUT")
        return asm

    @_('value')
    def expression(self, p):
        return p.value.get_value_asm

    @_('value PLUS value')
    def expression(self, p):
        return self.code_generator.add(p.value0, p.value1)

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
        val_content = p.NUM
        return ValueAttr(self.code_generator.generate_constant(val_content), "const", val_content)

    @_('identifier')
    def value(self, p):
        asm, var_name = p.identifier.var_address_asm, p.identifier.var_name
        try:
            asm += self.code_generator.load_variable_value(var_name)
        except Exception as e:
            raise CompilerException(e)
        return ValueAttr(asm, "var", var_name)

    @_('PIDENTIFIER')
    def identifier(self, p):
        try:
            var_name = p.PIDENTIFIER
            asm = self.code_generator.get_var_address(var_name)
            return IdentifierAttr(asm, var_name)
        except Exception as e:
            raise CompilerException(e, p.lineno)

    # @_('PIDENTIFIER "[" PIDENTIFIER "]"')
    # def identifier(self, p):
    #     pass
    #
    # @_('PIDENTIFIER "[" NUM "]"')
    # def identifier(self, p):
    #     pass


def main():
    lexer = CompilerLexer()
    parser = CompilerParser()

    if len(sys.argv) != 3:
        raise Exception("usage: python3.8 CompilerParser.py <input_file> <output_file>")

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    with open(input_file) as f:
        code = f.read()
    lexer_tokenize = lexer.tokenize(code)
    # print("LEXER RESULT:")
    # for tok in tokenize_res:
    #     print(tok)
    # print("================")
    result = parser.parse(lexer_tokenize)
    print(result)
    result = '\n'.join(result)
    print(parser.symbol_table)
    # print(result)
    with open(output_file, 'w') as f:
        f.write(result)


if __name__ == '__main__':
    main()