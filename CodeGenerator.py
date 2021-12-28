class CodeGenerator:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    # REGISTER: a, b
    def generate_const(self, number):
        asm = []
        reg_1 = 'b'
        instr = "INC" if number >= 0 else "DEC"

        binary = f'{abs(number):b}'
        asm.append("RESET a")
        asm.append(f"RESET {reg_1}")
        asm.append(f"INC {reg_1}")
        for bit in binary[:-1]:
            if bit == '1':
                asm.append(f"{instr} a")
            asm.append(f"SHIFT {reg_1}")
        if binary[-1] == '1':
            asm.append(f"{instr} a")
        return asm

    # REGISTER: - + generate_const
    def get_var_address(self, var_name):
        if var_name not in self.symbol_table:
            raise Exception(f"Access to undeclared variable {var_name}")

        return self.generate_const(self.symbol_table[var_name].address)

    # REGISTER: a, h
    def load_var_value(self, var_name):
        if not self.symbol_table[var_name].initialized:
            raise Exception(f"Access to uninitialized variable {var_name}")

        asm = []
        reg_address = 'h'

        asm.append(f"SWAP {reg_address}")
        asm.append(f"LOAD {reg_address}")
        return asm

    # REGISTER: a, h
    def store_var_value(self, var_name):
        asm = []
        reg_address = 'h'

        asm.append(f"SWAP {reg_address}")
        asm.append("GET")
        asm.append(f"STORE {reg_address}")

        self.symbol_table[var_name].initialized = True
        return asm

    # REGISTER: a, g
    def assign(self, identifier_attr, assigned_expression_asm):
        asm = []
        reg_aux = 'g'

        asm += assigned_expression_asm
        asm.append(f"SWAP {reg_aux}")

        var_address_asm, var_name = identifier_attr.var_address_asm, identifier_attr.var_name
        asm += var_address_asm
        asm.append(f"SWAP {reg_aux}")

        asm.append(f"STORE {reg_aux}")

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
            asm += self.generate_const(const1 + const2)
        else:
            reg_aux = 'g'
            asm += value_attr_2.get_value_asm
            asm.append(f"SWAP {reg_aux}")
            asm += value_attr_1.get_value_asm
            asm.append(f"ADD {reg_aux}")

        return asm

    # REGISTER: a, g
    def sub(self, value_attr_1, value_attr_2):
        asm = []

        type1 = value_attr_1.value_type
        type2 = value_attr_2.value_type
        if type1 == "const" and type2 == "const":
            const1 = value_attr_1.value_content
            const2 = value_attr_2.value_content
            asm += self.generate_const(const1 - const2)
        else:
            reg_aux = 'g'
            asm += value_attr_2.get_value_asm
            asm.append(f"SWAP {reg_aux}")
            asm += value_attr_1.get_value_asm
            asm.append(f"SUB {reg_aux}")

        return asm

    # REGISTER: a, b, c, d, e, f, g
    def mul(self, value_attr_1, value_attr_2):
        asm = []

        type1 = value_attr_1.value_type
        type2 = value_attr_2.value_type
        if type1 == "const" and type2 == "const":
            const1 = value_attr_1.value_content
            const2 = value_attr_2.value_content
            asm += self.generate_const(const1 * const2)
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
        reg_expo = 'c'

        if const == 0:
            asm.append("RESET a")
        elif const == 1:
            asm += get_var_asm
        elif const == -1:
            reg_aux = 'b'

            asm += get_var_asm
            asm.append(f"SWAP {reg_aux}")
            asm.append("RESET a")
            asm.append(f"SUB {reg_aux}")
        elif const == 2:
            asm += get_var_asm
            asm.append(f"RESET {reg_expo}")
            asm.append(f"INC {reg_expo}")
            asm.append(f"SHIFT {reg_expo}")
        elif const == -2:
            reg_aux = 'b'

            asm += get_var_asm
            asm.append(f"RESET {reg_expo}")
            asm.append(f"INC {reg_expo}")
            asm.append(f"SHIFT {reg_expo}")
            asm.append(f"SWAP {reg_aux}")
            asm.append(f"RESET a")
            asm.append(f"SUB {reg_aux}")
        else:
            reg_rec_res = 'b'
            reg_var = 'g'
            instr = "ADD" if const >= 0 else "SUB"

            asm += get_var_asm
            asm.append(f"SWAP {reg_var}")  # value of var saved in register g
            asm.append("RESET a")
            asm.append(f"{instr} {reg_var}")
            asm.append(f"RESET {reg_rec_res}")
            asm.append(f"RESET {reg_expo}")
            binary = f'{abs(const):b}'
            n = len(binary)
            first_one_read = False
            for i in range(n - 1, -1, -1):
                if binary[i] == '1':
                    if not first_one_read:
                        first_one_read = True
                        if i != n - 1:  # because we don't need to multiply register a by 1
                            asm.append(f"SHIFT {reg_expo}")
                    else:
                        asm.append(f"SWAP {reg_rec_res}")
                        asm.append("RESET a")
                        asm.append(f"{instr} {reg_var}")
                        asm.append(f"SHIFT {reg_expo}")
                        asm.append(f"ADD {reg_rec_res}")
                asm.append(f"INC {reg_expo}")
        return asm

    # REGISTER: a, b, c, d, e, f, g
    def mul_var_by_var(self, get_var_asm1, get_var_asm2):
        asm = []
        reg_aux1 = 'c'  # najpierw przechowuje 1 zmienną, potem przechowuje -1 do zamiany na system binarny
        reg_aux2 = 'b'  # najpierw przechowuje 2 zmienną, potem przechowuje wyniki związane z zamianą na system binarny
        reg_smaller = 'd'
        reg_expo = 'e'
        reg_rec_res = 'f'
        reg_sign = 'g'

        asm += get_var_asm1  # wczytanie 1. zmiennej
        asm.append(f"RESET {reg_sign}")  # jeżeli jest równy 0, to nie bedziemy zmieniac znaku mnozenia

        asm.append("JPOS 5")

        # wartość bezwzględna 1.zmiennej, jeśli jest niedodatnia
        asm.append(f"DEC {reg_sign}")
        asm.append(f"SWAP {reg_aux1}")
        asm.append("RESET a")
        asm.append(f"SUB {reg_aux1}")

        asm.append(f"SWAP {reg_aux1}")  # zapisanie 1. zmiennej w rejestrze reg_aux1

        asm += get_var_asm2  # wczytanie 2. zmiennej

        asm.append("JPOS 5")

        # wartość bezwzględna 2.zmiennej, jeśli jest ujemna
        asm.append(f"INC {reg_sign}")
        asm.append(f"SWAP {reg_aux2}")
        asm.append("RESET a")
        asm.append(f"SUB {reg_aux2}")

        asm.append(f"SWAP {reg_aux2}")  # zapisanie 2. zmiennej w rejestrze reg_aux2

        # sprawdzenie, która liczba ma mniejszą wartość bezwzględną
        asm.append("RESET a")
        asm.append(f"ADD {reg_aux1}")
        asm.append(f"SUB {reg_aux2}")
        asm.append("JNEG 6")
        asm.append(f"SWAP {reg_aux1}")
        asm.append(f"SWAP {reg_smaller}")
        asm.append("RESET a")
        asm.append(f"ADD {reg_aux2}")
        asm.append("JUMP 5")
        asm.append(f"SWAP {reg_aux2}")
        asm.append(f"SWAP {reg_smaller}")
        asm.append("RESET a")
        asm.append(f"ADD {reg_aux1}")
        # teraz w rejestrze a mamy większą liczbę z 2 wczytanych
        asm.append(f"RESET {reg_aux1}")
        asm.append(f"DEC {reg_aux1}")  # -1 do dzielenia przez 2
        asm.append(f"RESET {reg_expo}")  # wykladnik potęgi
        asm.append(f"RESET {reg_rec_res}")  # aktualny wynik mnożenia

        asm.append(f"SWAP {reg_aux2}")
        asm.append("RESET a")
        asm.append(f"ADD {reg_aux2}")
        asm.append(f"SHIFT {reg_aux1}")
        asm.append(f"SWAP {reg_aux2}")
        asm.append(f"SUB {reg_aux2}")
        asm.append(f"SUB {reg_aux2}")

        asm.append("JZERO 8")

        asm.append("RESET a")
        asm.append(f"ADD {reg_smaller}")
        asm.append(f"SHIFT {reg_expo}")  # mnożymy przez odpowiednią potęgę dwójki
        asm.append(f"ADD {reg_rec_res}")  # dodajemy poprzedni wynik
        asm.append(f"SWAP {reg_rec_res}")
        asm.append("RESET a")
        asm.append("INC a")

        asm.append(f"INC {reg_expo}")
        asm.append(f"SWAP {reg_aux2}")
        asm.append("JPOS -17")

        asm.append(f"SWAP {reg_sign}")

        asm.append("JZERO 6")

        # zmienianie znaku wyniku na ujemny, jeśli potrzeba
        asm.append(f"SWAP {reg_rec_res}")
        asm.append(f"SWAP {reg_aux2}")
        asm.append("RESET a")
        asm.append(f"SUB {reg_aux2}")
        asm.append("JUMP 2")

        asm.append(f"SWAP {reg_rec_res}")

        return asm
