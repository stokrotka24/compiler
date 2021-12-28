class CodeGenerator:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    # REGISTER: a, b
    def generate_constant(self, number):
        asm = []
        instr = "INC" if number >= 0 else "DEC"

        binary = f'{abs(number):b}'
        asm.append("RESET a")
        asm.append("RESET b")
        asm.append("INC b")
        for bit in binary[:-1]:
            if bit == '1':
                asm.append(f"{instr} a")
            asm.append("SHIFT b")
        if binary[-1] == '1':
            asm.append(f"{instr} a")
        return asm

    # REGISTER: a, b
    def get_var_address(self, variable_name):
        if variable_name not in self.symbol_table:
            raise Exception(f"Access to undeclared variable {variable_name}")

        return self.generate_constant(self.symbol_table[variable_name].address)

    # REGISTER: a, h
    def load_variable_value(self, variable_name):
        if not self.symbol_table[variable_name].initialized:
            raise Exception(f"Access to uninitialized variable {variable_name}")

        asm = []
        asm.append("SWAP h")
        asm.append("LOAD h")
        return asm

    # REGISTER: a, h
    def store_variable_value(self, variable_name):
        asm = []
        asm.append("SWAP h")
        asm.append("GET")
        asm.append("STORE h")

        self.symbol_table[variable_name].initialized = True
        return asm

    # REGISTER: a, g
    def assign(self, identifier_attr, assigned_expression_asm):
        asm = []

        asm += assigned_expression_asm
        asm.append("SWAP g")

        var_address_asm, var_name = identifier_attr.var_address_asm, identifier_attr.var_name
        asm += var_address_asm
        asm.append("SWAP g")

        asm.append("STORE g")

        self.symbol_table[var_name].initialized = True
        return asm

    # REGISTER: a, g
    def add(self, value_attr_1, value_attr_2):
        asm = []

        type1 = value_attr_1.value_type
        type2 = value_attr_2.value_type
        if type1 == "const" and type2 == "const":
            const1 = value_attr_1.value_content
            const2 = value_attr_2.value_content
            asm += self.generate_constant(const1 + const2)
        else:
            asm += value_attr_2.get_value_asm
            asm.append("SWAP g")
            asm += value_attr_1.get_value_asm
            asm.append("ADD g")

        return asm

    # REGISTER: a, g
    def sub(self, value_attr_1, value_attr_2):
        asm = []

        type1 = value_attr_1.value_type
        type2 = value_attr_2.value_type
        if type1 == "const" and type2 == "const":
            const1 = value_attr_1.value_content
            const2 = value_attr_2.value_content
            asm += self.generate_constant(const1 - const2)
        else:
            asm += value_attr_2.get_value_asm
            asm.append("SWAP g")
            asm += value_attr_1.get_value_asm
            asm.append("SUB g")

        return asm

    # REGISTER: a, b, c, g
    def mul(self, value_attr_1, value_attr_2):
        asm = []

        type1 = value_attr_1.value_type
        type2 = value_attr_2.value_type
        if type1 == "const" and type2 == "const":
            const1 = value_attr_1.value_content
            const2 = value_attr_2.value_content
            asm += self.generate_constant(const1 * const2)
        elif type1 == "var" and type2 == "const":
            const = value_attr_2.value_content
            if const == 0:
                asm.append("RESET a")
            else:
                instr = "ADD" if const >= 0 else "SUB"
                asm += value_attr_1.get_value_asm
                asm.append("SWAP g")  # value of var saved in register g
                asm.append("RESET a")
                asm.append(f"{instr} g")
                asm.append("RESET b")
                asm.append("RESET c")
                binary = f'{abs(const):b}'
                n = len(binary)
                first_one_read = False
                for i in range(n - 1, -1, -1):
                    if binary[i] == '1':
                        if not first_one_read:
                            first_one_read = True
                            if i != n - 1:  # because we don't need to multiply by 1
                                asm.append("SHIFT c")
                        else:
                            asm.append("SWAP b")
                            asm.append("RESET a")
                            asm.append(f"{instr} g")
                            asm.append("SHIFT c")
                            asm.append("ADD b")
                    asm.append("INC c")
        return asm
