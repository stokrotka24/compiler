from CompilerException import CompilerException


class CodeGenerator:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    # used regs: a, b
    def generate_constant(self, number):
        asm = ""
        instr = "INC" if number >= 0 else "DEC"

        binary = f'{abs(number):b}'
        asm += "RESET a\n"
        asm += "RESET b\n"
        asm += "INC b\n"
        for bit in binary[:-1]:
            if bit == '1':
                asm += f"{instr} a\n"
            asm += "SHIFT b\n"
        if binary[-1] == '1':
            asm += f"{instr} a\n"
        return asm

    # used -
    def load_variable_address(self, variable_name):
        if variable_name not in self.symbol_table:
            raise Exception(f"Access to undeclared variable {variable_name}")

        return self.generate_constant(self.symbol_table[variable_name].address)

    # used + h
    def load_variable_value(self, variable_name):
        if not self.symbol_table[variable_name].initialized:
            raise Exception(f"Access to uninitialized variable {variable_name}")

        asm = ""
        asm += "SWAP h\n"
        asm += "LOAD h\n"
        return asm

    # used + h
    def store_variable_value(self, variable_name):
        asm = ""
        asm += "SWAP h\n"
        asm += "GET\n"
        asm += "STORE h\n"

        self.symbol_table[variable_name].initialized = True
        return asm

