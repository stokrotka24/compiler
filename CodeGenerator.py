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

    # REGISTER: a, b, c, d, e, f, g
    def mul(self, value_attr_1, value_attr_2):
        asm = []

        type1 = value_attr_1.value_type
        type2 = value_attr_2.value_type
        if type1 == "const" and type2 == "const":
            const1 = value_attr_1.value_content
            const2 = value_attr_2.value_content
            asm += self.generate_constant(const1 * const2)
        elif type1 == "var" and type2 == "const":
            asm += self.mul_var_by_const(value_attr_1.get_value_asm, value_attr_2.value_content)
        elif type1 == "const" and type2 == "var":
            asm += self.mul_var_by_const(value_attr_2.get_value_asm, value_attr_1.value_content)
        else:
            asm += self.mul_var_by_var(value_attr_1.get_value_asm, value_attr_2.get_value_asm)

        return asm

    # REGISTER: a, b, c, g,
    def mul_var_by_const(self, get_var_asm, const):
        asm = []
        if const == 0:
            asm.append("RESET a")
        elif const == 1:
            asm += get_var_asm
        elif const == -1:
            asm += get_var_asm
            asm.append("SWAP b")
            asm.append("RESET a")
            asm.append("SUB b")
        elif const == 2:
            asm += get_var_asm
            asm.append("RESET c")
            asm.append("INC c")
            asm.append("SHIFT c")
        elif const == -2:
            asm += get_var_asm
            asm.append("RESET c")
            asm.append("INC c")
            asm.append("SHIFT c")
            asm.append("SWAP b")
            asm.append("RESET a")
            asm.append("SUB b")
        else:
            instr = "ADD" if const >= 0 else "SUB"
            asm += get_var_asm
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
                        if i != n - 1:  # because we don't need to multiply register a by 1
                            asm.append("SHIFT c")
                    else:
                        asm.append("SWAP b")
                        asm.append("RESET a")
                        asm.append(f"{instr} g")
                        asm.append("SHIFT c")
                        asm.append("ADD b")
                asm.append("INC c")
        return asm

    # REGISTER: a, b, c, d, e, f, g
    def mul_var_by_var(self, get_var_asm1, get_var_asm2):
        asm = []
        asm += get_var_asm1  # wczytanie 1. zmiennej
        asm.append("RESET g")  # jeżeli jest równy 0, to nie bedziemy zmieniac znaku mnozenia

        asm.append("JPOS 5")

        # wartość bezwzględna 1.zmiennej, jeśli jest niedodatnia
        asm.append("DEC g")
        asm.append("SWAP c")
        asm.append("RESET a")
        asm.append("SUB c")

        asm.append("SWAP c")  # zapisanie 1. zmiennej w rejestrze c

        asm += get_var_asm2  # wczytanie 2. zmiennej

        asm.append("JPOS 5")

        # wartość bezwzględna 2.zmiennej, jeśli jest ujemna
        asm.append("INC g")
        asm.append("SWAP b")
        asm.append("RESET a")
        asm.append("SUB b")

        asm.append("SWAP b")  # zapisanie 2. zmiennej w rejestrze b

        # sprawdzenie, która liczba ma mniejszą wartość bezwzględną
        asm.append("RESET a")
        asm.append("ADD c")
        asm.append("SUB b")
        asm.append("JNEG 6")
        asm.append("SWAP c")
        asm.append("SWAP d")
        asm.append("RESET a")
        asm.append("ADD b")
        asm.append("JUMP 5")
        asm.append("SWAP b")
        asm.append("SWAP d")
        asm.append("RESET a")
        asm.append("ADD c")
        # teraz w rejestrze a mamy większą liczbę z 2 wczytanych
        asm.append("RESET c")
        asm.append("DEC c")  # -1 do dzielenia przez 2
        asm.append("RESET e")  # wykladnik potęgi
        asm.append("RESET f")  # aktualny wynik mnożenia

        asm.append("SWAP b")
        asm.append("RESET a")
        asm.append("ADD b")
        asm.append("SHIFT c")
        asm.append("SWAP b")
        asm.append("SUB b")
        asm.append("SUB b")

        asm.append("JZERO 8")

        asm.append("RESET a")
        asm.append("ADD d")
        asm.append("SHIFT e")  # mnożymy przez odpowiednią potęgę dwójki
        asm.append("ADD f")  # dodajemy poprzedni wynik
        asm.append("SWAP f")
        asm.append("RESET a")
        asm.append("INC a")

        asm.append("INC e")
        asm.append("SWAP b")
        asm.append("JPOS -17")

        asm.append("SWAP g")

        asm.append("JZERO 6")

        # zmienianie znaku wyniku na ujemny, jeśli potrzeba
        asm.append("SWAP f")
        asm.append("SWAP b")
        asm.append("RESET a")
        asm.append("SUB b")
        asm.append("JUMP 2")
        asm.append("SWAP f")

        return asm
