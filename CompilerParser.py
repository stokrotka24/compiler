import sys

from sly import Parser
from CompilerLexer import CompilerLexer
from CompilerException import CompilerException
from CodeGenerator import CodeGenerator
from SymbolTable import SymbolTable, Variable
from ParserAttrs import IdentifierAttr, ValueAttr, ConditionAttr, ForAttr


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

    @_('declarations "," PIDENTIFIER "[" NUM ":" NUM "]"', 'PIDENTIFIER "[" NUM ":" NUM "]"')
    def declarations(self, p):
        message = self.symbol_table.array_declaration(p.PIDENTIFIER, p.NUM0, p.NUM1)
        if message:
            raise CompilerException(message, p.lineno)

    @_('commands command')
    def commands(self, p):
        return p.commands + p.command

    @_('command')
    def commands(self, p):
        return p.command

    @_('identifier ASSIGN expression ";"')
    def command(self, p):
        try:
            return self.code_generator.assign(p.identifier, p.expression)
        except Exception as e:
            raise CompilerException(e, p.lineno)

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        return self.code_generator.if_then_else(p.condition, p.commands0, p.commands1)

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        return self.code_generator.if_then(p.condition, p.commands)

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        return self.code_generator.while_do(p.condition, p.commands)

    @_('REPEAT commands UNTIL condition ";"')
    def command(self, p):
        return self.code_generator.repeat_until(p.condition, p.commands)

    @_('FOR PIDENTIFIER FROM value TO value',
       'FOR PIDENTIFIER FROM value DOWNTO value')
    def for_init(self, p):
        iterator_name = p.PIDENTIFIER

        try:
            global_var = self.code_generator.init_for(iterator_name)
        except Exception as e:
            raise CompilerException(e, p.lineno)

        self.symbol_table[iterator_name].initialized = True
        return ForAttr(iterator_name, p.value0, p.value1, global_var, p[4])

    @_('for_init DO commands ENDFOR')
    def command(self, p):
        for_type = p.for_init.for_type
        try:
            if for_type == "TO":
                return self.code_generator.for_to(p.for_init.pidentifier,
                                                  p.for_init.start_value_attr, p.for_init.end_value_attr,
                                                  p.for_init.global_var, p.commands)
            elif for_type == "DOWNTO":
                return self.code_generator.for_downto(p.for_init.pidentifier,
                                                      p.for_init.start_value_attr, p.for_init.end_value_attr,
                                                      p.for_init.global_var, p.commands)
            else:
                raise Exception("Not allowed for_type")
        except Exception as e:
            raise CompilerException(e, p.lineno)

    @_('READ identifier ";"')
    def command(self, p):
        identifier_type = p.identifier.identifier_type

        if identifier_type == "var":
            asm, var_name = p.identifier.identifier_address_asm, p.identifier.identifier_name
            if self.symbol_table[var_name].loop_iterator:
                raise CompilerException(f"Not allowed loop iterator {var_name} modification", p.lineno)

            asm += self.code_generator.store_var_value(var_name)
            return asm
        elif identifier_type == "arr":
            asm, arr_name = p.identifier.identifier_address_asm, p.identifier.identifier_name
            asm += self.code_generator.store_arr_elem_value()
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

    @_('value MINUS value')
    def expression(self, p):
        return self.code_generator.sub(p.value0, p.value1)

    @_('value TIMES value')
    def expression(self, p):
        return self.code_generator.mul(p.value0, p.value1)

    @_('value DIV value')
    def expression(self, p):
        return self.code_generator.div(p.value0, p.value1)

    @_('value MOD value')
    def expression(self, p):
        return self.code_generator.mod(p.value0, p.value1)

    @_('value EQ value')
    def condition(self, p):
        return ConditionAttr(self.code_generator.sub(p.value1, p.value0), "EQ")

    @_('value NEQ value')
    def condition(self, p):
        return ConditionAttr(self.code_generator.sub(p.value1, p.value0), "NEQ")

    @_('value LE value')
    def condition(self, p):
        return ConditionAttr(self.code_generator.sub(p.value1, p.value0), "LE")

    @_('value GE value')
    def condition(self, p):
        return ConditionAttr(self.code_generator.sub(p.value1, p.value0), "GE")

    @_('value LEQ value')
    def condition(self, p):
        return ConditionAttr(self.code_generator.sub(p.value1, p.value0), "LEQ")

    @_('value GEQ value')
    def condition(self, p):
        return ConditionAttr(self.code_generator.sub(p.value1, p.value0), "GEQ")

    @_('NUM')
    def value(self, p):
        val_content = p.NUM
        return ValueAttr(self.code_generator.generate_const(val_content), "const", val_content)

    @_('identifier')
    def value(self, p):
        identifier_type = p.identifier.identifier_type

        if identifier_type == "var":
            asm, var_name = p.identifier.identifier_address_asm, p.identifier.identifier_name
            try:
                asm += self.code_generator.load_var_value(var_name)
            except Exception as e:
                raise CompilerException(e)
            return ValueAttr(asm, "var", var_name)

        elif identifier_type == "arr":
            asm, arr_name = p.identifier.identifier_address_asm, p.identifier.identifier_name
            asm += self.code_generator.load_arr_elem_value()
            return ValueAttr(asm, "arr", arr_name)

        raise CompilerException("Unexpected type of identifier")

    @_('PIDENTIFIER')
    def identifier(self, p):
        try:
            var_name = p.PIDENTIFIER
            asm = self.code_generator.get_var_address(var_name)
            return IdentifierAttr(asm, "var", var_name)
        except Exception as e:
            raise CompilerException(e, p.lineno)

    @_('PIDENTIFIER "[" PIDENTIFIER "]"')
    def identifier(self, p):
        try:
            arr_name = p.PIDENTIFIER0
            var_name = p.PIDENTIFIER1

            asm = self.code_generator.get_arr_elem_address_with_var_index(arr_name, var_name)
            return IdentifierAttr(asm, "arr", arr_name)
        except Exception as e:
            raise CompilerException(e, p.lineno)

    @_('PIDENTIFIER "[" NUM "]"')
    def identifier(self, p):
        try:
            arr_name = p.PIDENTIFIER
            arr_index = p.NUM
            asm = self.code_generator.get_arr_elem_address(arr_name, arr_index)
            return IdentifierAttr(asm, "arr", arr_name)
        except Exception as e:
            raise CompilerException(e, p.lineno)

    def error(self, p):
        raise CompilerException(f"Syntax error at token {p.type}", p.lineno)


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
    try:
        result = parser.parse(lexer_tokenize)
    except CompilerException as ex:
        print(ex)
        sys.exit()
    print(result)
    result = '\n'.join(result)
    # print(result)
    print(parser.symbol_table)
    # print(result)
    with open(output_file, 'w') as f:
        f.write(result)


if __name__ == '__main__':
    main()
