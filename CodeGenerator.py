from SymbolTable import Variable, Array


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

        variable = self.symbol_table[var_name]
        if type(variable) is Array:
            raise Exception(f"{var_name} is an array, not a variable")

        return self.generate_const(variable.address)

    # REGISTER: - + generate_const
    def get_arr_elem_address(self, arr_name, arr_index):
        if arr_name not in self.symbol_table:
            raise Exception(f"Access to undeclared array {arr_name}")
        arr = self.symbol_table[arr_name]

        if type(arr) is Variable:
            raise Exception(f"{arr_name} is a variable, not an array")

        if arr_index < arr.first_index or arr_index > arr.last_index:
            raise Exception(
                f"Access to index {arr_index} in array {arr_name}, which has range [{arr.first_index}, {arr.last_index}]")

        return self.generate_const(arr.address + arr_index - arr.first_index)

    def get_arr_elem_address_with_var_index(self, arr_name, var_name):
        if arr_name not in self.symbol_table:
            raise Exception(f"Access to undeclared array {arr_name}")

        arr = self.symbol_table[arr_name]
        if type(arr) is Variable:
            raise Exception(f"{arr_name} is a variable, not an array")

        asm = []

        asm += self.get_var_address(var_name)  # REGISTER a, b
        asm += self.load_var_value(var_name)  # REGISTER a, h
        asm.append("SWAP h")  # save value of var in register h

        asm += self.generate_const(arr.first_index)  # REGISTER a, b

        # calculate order of elem array[var's value] in array
        asm.append("SUB h")
        asm.append("SWAP h")
        asm.append("RESET a")
        asm.append("SUB h")

        asm.append("SWAP h")  # save order of elem array[var's value] in array in register h

        asm += self.generate_const(arr.address)  # REGISTER a, b
        asm.append("ADD h")
        return asm

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
    def load_arr_elem_value(self):
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

    # REGISTER: a, h
    def store_arr_elem_value(self):
        asm = []
        reg_address = 'h'

        asm.append(f"SWAP {reg_address}")
        asm.append("GET")
        asm.append(f"STORE {reg_address}")
        return asm

    # REGISTER: a, h
    def assign(self, identifier_attr, assigned_expression_asm):
        asm = []
        reg_aux = 'd'  # can't use h, because in a[n] ASSIGN 1, h is used to do a[n]

        asm += assigned_expression_asm
        asm.append(f"SWAP {reg_aux}")

        identifier_address_asm = identifier_attr.identifier_address_asm
        asm += identifier_address_asm
        asm.append(f"SWAP {reg_aux}")
        asm.append(f"STORE {reg_aux}")

        identifier_type = identifier_attr.identifier_type

        if identifier_type == "var":
            var_name = identifier_attr.identifier_name

            if self.symbol_table[var_name].loop_iterator:
                raise Exception(f"Not allowed loop iterator {var_name} modification")

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

        asm.append("JZERO 4")

        # zmienianie znaku wyniku na ujemny, jeśli potrzeba
        asm.append("RESET a")
        asm.append(f"SUB {reg_rec_res}")
        asm.append("JUMP 2")

        asm.append(f"SWAP {reg_rec_res}")

        return asm

    # REGISTER: a, b, c, d, e, f, g
    def div(self, value_attr_1, value_attr_2):
        asm = []

        type1 = value_attr_1.value_type
        type2 = value_attr_2.value_type
        if type1 == "const" and type2 == "const":
            const1 = value_attr_1.value_content
            const2 = value_attr_2.value_content
            if const2 != 0:
                asm += self.generate_const(const1 // const2)
            else:
                asm.append("RESET a")
        else:
            asm += self.div_var_by_var(value_attr_1.get_value_asm, value_attr_2.get_value_asm)

        return asm

    def div_var_by_var(self, get_var_asm1, get_var_asm2):
        reg_counter = 'c'  # counter in PART_1, PART_2
        reg_const = 'd'  # 1 in PART_1, -1 in PART_2
        reg_quotient = 'f'
        reg_flag = 'g'  # 0, if there is no need change quotient
        reg_dividend = 'e'  # =/= a, b, h, because they are used to load divisor
        reg_divisor = 'b'

        asm = []
        asm.append(f"RESET {reg_counter}")
        asm.append(f"DEC {reg_counter}")

        asm.append(f"RESET {reg_const}")
        asm.append(f"INC {reg_const}")

        asm.append(f"RESET {reg_quotient}")
        asm.append(f"RESET {reg_flag}")

        asm += get_var_asm1  # get dividend, REGISTER: a, b, h

        asm.append(f"JZERO {65 + len(get_var_asm2)}")  # -> END
        asm.append("JPOS 5")  # no need set dividend flag
        asm.append(f"DEC {reg_flag}")  # set flag that dividend < 0
        asm.append(f"SWAP {reg_dividend}")
        asm.append("RESET a")
        asm.append(f"SUB {reg_dividend}")

        asm.append(f"SWAP {reg_dividend}")  # save |dividend|

        asm += get_var_asm2  # get divisor, REGISTER: a, b, h

        asm.append("JZERO 58")  # -> END
        asm.append("JPOS 5")  # no need set divisor flag
        asm.append(f"INC {reg_flag}")  # set flag that divisor < 0
        asm.append(f"SWAP {reg_divisor}")
        asm.append("RESET a")
        asm.append(f"SUB {reg_divisor}")

        asm.append(f"SWAP {reg_divisor}")  # save |divisor|

        asm.append("RESET a")
        asm.append(f"ADD {reg_divisor}")
        asm.append(f"SUB {reg_dividend}")
        asm.append("JPOS 2")  # |dividend| < |divisor|
        asm.append("JUMP 3")  # |dividend| >= |divisor|
        asm.append("RESET a")
        asm.append("JUMP 33")  # |dividend| < |divisor|, -> CHANGE_QUOTIENT

        # PART_1
        asm.append(f"ADD {reg_divisor}")
        asm.append(f"SWAP {reg_divisor}")
        asm.append(f"SHIFT {reg_const}")
        asm.append(f"INC {reg_counter}")

        asm.append(f"SWAP {reg_divisor}")
        asm.append("JPOS 2")
        asm.append("JUMP -6")  # divisor <= dividend, -> PART_1

        asm.append(f"RESET {reg_const}")
        asm.append(f"DEC {reg_const}")

        asm.append(f"SWAP {reg_divisor}")
        asm.append(f"SHIFT {reg_const}")  # divisor // 2
        asm.append(f"SWAP {reg_divisor}")  # save divisor

        # PART_2
        asm.append("RESET a")
        asm.append(f"ADD {reg_dividend}")
        asm.append(f"SUB {reg_divisor}")
        asm.append("JNEG 7")  # dividend < divisor, -> UPDATE
        asm.append(f"SWAP {reg_dividend}")  # dividend = dividend - divisor
        asm.append("RESET a")  # in REGISTER there is an obsolete dividend, we don't need it no more
        asm.append("INC a")
        asm.append(f"SHIFT {reg_counter}")
        asm.append(f"ADD {reg_quotient}")
        asm.append(f"SWAP {reg_quotient}")  # quotient = quotient + 2^(counter)

        # UPDATE
        asm.append(f"SWAP {reg_divisor}")
        asm.append(f"SHIFT {reg_const}")  # divisor // 2
        asm.append(f"SWAP {reg_divisor}")  # save divisor

        asm.append(f"DEC {reg_counter}")
        asm.append("RESET a")
        asm.append("DEC a")
        asm.append(f"SUB {reg_counter}")
        asm.append("JNEG -17")  # REGISTER c =/= -1, -> PART_2

        asm.append(f"SWAP {reg_dividend}")  # rest
        asm.append("JZERO 7")  # rest = 0, -> EXCEPTION_CHANGE_QUOTIENT

        # CHANGE_QUOTIENT
        asm.append(f"SWAP {reg_flag}")
        asm.append("JZERO 10")  # -> NO_CHANGE_QUOTIENT
        asm.append("RESET a")
        asm.append(f"SUB {reg_quotient}")
        asm.append("DEC a")
        asm.append("JUMP 7")  # -> END

        # EXCEPTION_CHANGE_QUOTIENT
        asm.append(f"SWAP {reg_flag}")
        asm.append("JZERO 4")  # -> NO_CHANGE_QUOTIENT
        asm.append("RESET a")
        asm.append(f"SUB {reg_quotient}")
        asm.append("JUMP 2")  # -> END

        # NO_CHANGE_QUOTIENT
        asm.append(f"SWAP {reg_quotient}")

        # END

        return asm

    # REGISTER: a, b, c, d, e, f, g, h
    def mod(self, value_attr_1, value_attr_2):
        asm = []

        type1 = value_attr_1.value_type
        type2 = value_attr_2.value_type
        if type1 == "const" and type2 == "const":
            const1 = value_attr_1.value_content
            const2 = value_attr_2.value_content
            if const2 != 0:
                asm += self.generate_const(const1 % const2)
            else:
                asm.append("RESET a")
        else:
            asm += self.mod_var_by_var(value_attr_1.get_value_asm, value_attr_2.get_value_asm)

        return asm

    def mod_var_by_var(self, get_var_asm1, get_var_asm2):
        reg_counter = 'c'  # counter in PART_1, PART_2
        reg_const = 'd'  # 1 in PART_1, -1 in PART_2
        reg_dividend_flag = 'f'  # 1 if dividend < 0, 0 otherwise
        reg_divisor_flag = 'g'  # 1 if divisor < 0, 0 otherwise
        reg_dividend = 'e'  # =/= a, b, h, because they are used to load divisor
        reg_divisor = 'b'
        reg_divisor_abs = 'h'  # |divisor| needed for changing rest

        asm = []
        asm.append(f"RESET {reg_counter}")
        asm.append(f"DEC {reg_counter}")

        asm.append(f"RESET {reg_const}")
        asm.append(f"INC {reg_const}")

        asm.append(f"RESET {reg_dividend_flag}")
        asm.append(f"RESET {reg_divisor_flag}")

        asm += get_var_asm1  # get dividend, REGISTER: a, b, h

        asm.append(f"JZERO {69 + len(get_var_asm2)}")  # -> END
        asm.append("JPOS 5")  # no need set dividend flag
        asm.append(f"INC {reg_dividend_flag}")  # set flag that dividend < 0
        asm.append(f"SWAP {reg_dividend}")
        asm.append("RESET a")
        asm.append(f"SUB {reg_dividend}")

        asm.append(f"SWAP {reg_dividend}")  # save |dividend|

        asm += get_var_asm2  # get divisor, REGISTER: a, b, h

        asm.append("JZERO 62")  # -> END
        asm.append("JPOS 5")  # no need set divisor flag
        asm.append(f"INC {reg_divisor_flag}")  # set flag that divisor < 0
        asm.append(f"SWAP {reg_divisor}")
        asm.append("RESET a")
        asm.append(f"SUB {reg_divisor}")

        asm.append(f"SWAP {reg_divisor}")  # save |divisor|
        asm.append(f"RESET a")
        asm.append(f"ADD {reg_divisor}")
        asm.append(f"SWAP {reg_divisor_abs}")

        asm.append("RESET a")
        asm.append(f"ADD {reg_divisor}")
        asm.append(f"SUB {reg_dividend}")
        asm.append("JPOS 2")  # |dividend| < |divisor|
        asm.append("JUMP 3")  # |dividend| >= |divisor|
        asm.append("RESET a")
        asm.append("JUMP 26")  # |dividend| < |divisor|, -> CHANGE_REST

        # PART_1
        asm.append(f"ADD {reg_divisor}")
        asm.append(f"SWAP {reg_divisor}")
        asm.append(f"SHIFT {reg_const}")
        asm.append(f"INC {reg_counter}")

        asm.append(f"SWAP {reg_divisor}")
        asm.append("JPOS 2")
        asm.append("JUMP -6")  # divisor <= dividend, -> PART_1

        asm.append(f"RESET {reg_const}")
        asm.append(f"DEC {reg_const}")

        asm.append(f"SWAP {reg_divisor}")
        asm.append(f"SHIFT {reg_const}")  # divisor // 2
        asm.append(f"SWAP {reg_divisor}")  # save divisor

        # PART_2
        asm.append("RESET a")
        asm.append(f"ADD {reg_dividend}")
        asm.append(f"SUB {reg_divisor}")
        asm.append("JNEG 2")  # dividend < divisor, -> UPDATE
        asm.append(f"SWAP {reg_dividend}")  # dividend = dividend - divisor

        # UPDATE
        asm.append(f"SWAP {reg_divisor}")
        asm.append(f"SHIFT {reg_const}")  # divisor // 2
        asm.append(f"SWAP {reg_divisor}")  # save divisor

        asm.append(f"DEC {reg_counter}")
        asm.append("RESET a")
        asm.append("DEC a")
        asm.append(f"SUB {reg_counter}")
        asm.append("JNEG -12")  # REGISTER c =/= -1, -> PART_2

        # CHANGE_REST
        asm.append(f"SWAP {reg_dividend_flag}")
        asm.append("JZERO 12")  # -> DIVIDEND_NONNEG

        # DIVIDEND_NEG
        asm.append(f"SWAP {reg_divisor_flag}")
        asm.append("JZERO 4")  # -> DIVIDEND_NEG, DIVISOR_NONNEG

        # DIVIDEND_NEG, DIVISOR_NEG ( rest = - rest )
        asm.append("RESET a")
        asm.append(f"SUB {reg_dividend}")
        asm.append("JUMP 14")  # -> END

        # DIVIDEND_NEG, DIVISOR_NONNEG ( rest = |divisor| - rest )
        asm.append(f"SWAP {reg_dividend}")
        asm.append("JZERO 12")  # rest = 0, no need to change rest, -> END
        asm.append(f"SWAP {reg_dividend}")
        asm.append(f"ADD {reg_divisor_abs}")
        asm.append(f"SUB {reg_dividend}")
        asm.append("JUMP 8")  # -> END

        # DIVIDEND_NONNEG
        asm.append(f"SWAP {reg_divisor_flag}")
        asm.append("JZERO 5")  # -> DIVIDEND_NONNEG, DIVISOR_NONENEG

        # DIVIDEND_NONNEG, DIVISOR_NEG ( rest = rest - |divisor| )
        asm.append(f"SWAP {reg_dividend}")
        asm.append("JZERO 4")  # rest = 0, no need to change rest, -> END
        asm.append(f"SUB {reg_divisor_abs}")
        asm.append("JUMP 2")  # -> END

        # DIVIDEND_NONNEG, DIVISOR_NONNEG ( rest = rest )
        asm.append(f"SWAP {reg_dividend}")

        # END

        return asm

    def if_then(self, cond_attr, commands_asm):
        asm = []
        asm += cond_attr.get_difference_asm  # now in reg a is diff: val2 - val1
        asm += self.condition_false_forward_asm(cond_attr.condition_type, len(commands_asm))
        asm += commands_asm

        return asm

    def if_then_else(self, cond_attr, commands1_asm, commands2_asm):
        asm = []
        asm += cond_attr.get_difference_asm  # now in reg a is diff: val2 - val1
        asm += self.condition_false_forward_asm(cond_attr.condition_type, len(commands1_asm) + 1)
        asm += commands1_asm
        asm.append(f"JUMP {len(commands2_asm) + 1}")
        asm += commands2_asm

        return asm

    def condition_false_forward_asm(self, condition_type, commands_asm_len):
        if condition_type == "EQ":
            return [f"JPOS {commands_asm_len + 2}", f"JNEG {commands_asm_len + 1}"]
        elif condition_type == "NEQ":
            return [f"JZERO {commands_asm_len + 1}"]
        elif condition_type == "LE":
            return [f"JNEG {commands_asm_len + 2}", f"JZERO {commands_asm_len + 1}"]
        elif condition_type == "GE":
            return [f"JPOS {commands_asm_len + 2}", f"JZERO {commands_asm_len + 1}"]
        elif condition_type == "LEQ":
            return [f"JNEG {commands_asm_len + 1}"]
        elif condition_type == "GEQ":
            return [f"JPOS {commands_asm_len + 1}"]
        else:
            raise Exception(f"Inproper condition type: {condition_type}")

    def condition_false_back_asm(self, condition_type, commands_asm_len):
        if condition_type == "EQ":
            return [f"JPOS -{commands_asm_len}", f"JNEG -{commands_asm_len + 1}"]
        elif condition_type == "NEQ":
            return [f"JZERO -{commands_asm_len}"]
        elif condition_type == "LE":
            return [f"JNEG -{commands_asm_len}", f"JZERO -{commands_asm_len + 1}"]
        elif condition_type == "GE":
            return [f"JPOS -{commands_asm_len}", f"JZERO -{commands_asm_len + 1}"]
        elif condition_type == "LEQ":
            return [f"JNEG -{commands_asm_len}"]
        elif condition_type == "GEQ":
            return [f"JPOS -{commands_asm_len}"]
        else:
            raise Exception(f"Inproper condition type: {condition_type}")

    def while_do(self, cond_attr, commands_asm):
        asm = []
        asm += cond_attr.get_difference_asm
        asm += self.condition_false_forward_asm(cond_attr.condition_type, len(commands_asm) + 1)
        asm += commands_asm
        asm.append(f"JUMP -{len(asm) + 1}")

        return asm

    def repeat_until(self, cond_attr, commands_asm):
        asm = []
        asm += commands_asm
        asm += cond_attr.get_difference_asm
        asm += self.condition_false_back_asm(cond_attr.condition_type, len(asm))

        return asm

    def init_for(self, iterator_name):
        # if there is a global variable/array with the same name, we have to override it, but save global variable/array
        global_var = self.symbol_table.pop(iterator_name, None)
        if global_var and global_var.loop_iterator:
            raise Exception(f"Not allowed reuse of loop iterator {iterator_name} as a loop iterator")

        self.symbol_table.loop_iterator_declaration(iterator_name)
        return global_var

    def for_to(self, iterator_name, start_value_attr, end_value_attr, global_var, commands_asm):
        asm = []
        reg_aux = 'd'
        reg_address = 'h'

        iterator_address = self.symbol_table[iterator_name].address

        type1 = start_value_attr.value_type
        type2 = end_value_attr.value_type
        if type1 == "const" and type2 == "const":
            start_value = start_value_attr.value_content
            end_value = end_value_attr.value_content

            if start_value <= end_value:
                for i_value in range(start_value, end_value + 1):
                    asm += self.generate_const(iterator_address)
                    asm.append(f"SWAP {reg_address}")
                    asm += self.generate_const(i_value)
                    asm.append(f"STORE {reg_address}")
                    asm += commands_asm

        else:
            if type1 == "var" and start_value_attr.value_content == iterator_name:
                raise Exception(f"Iterator {iterator_name} can't be as one of range of loop")
            if type2 == "var" and end_value_attr.value_content == iterator_name:
                raise Exception(f"Iterator {iterator_name} can't be as one of range of loop")

            len_commands_asm = len(commands_asm)

            gen_it_add = self.generate_const(iterator_address)
            len_gen_it_add = len(gen_it_add)

            lev_address, lev_name = self.symbol_table.loop_end_value_declaration()
            gen_lev_add = self.generate_const(lev_address)
            len_gen_lev_add = len(gen_lev_add)

            len_snippets = len_commands_asm + len_gen_it_add + len_gen_lev_add

            asm += start_value_attr.get_value_asm  # REGISTER a, b, h
            asm.append(f"SWAP {reg_address}")  # save start_value in REGISTER reg_address

            asm += gen_it_add  # generate address of iterator, REGISTER a, b
            asm.append(f"SWAP {reg_address}")  # start_value in REGISTER a, iterator_address in register reg_address
            asm.append(f"STORE {reg_address}")  # save start value of iterator
            asm.append(f"SWAP {reg_aux}")  # save start_value in REGISTER reg_aux

            asm += end_value_attr.get_value_asm  # REGISTER a, b, h
            asm.append(f"SWAP {reg_address}")  # save end_value in REGISTER reg_address

            asm += gen_lev_add
            asm.append(f"SWAP {reg_address}")  # lev_address in REGISTER reg_address, end_value in REGISTER a
            asm.append(f"STORE {reg_address}")  # save value of lev

            asm.append(f"SUB {reg_aux}")  # end_value - start_value

            asm.append(f"JNEG {11 + len_snippets}")  # omit loop, because start_value > end_value
            asm.append(f"JUMP {10 + len_gen_it_add + len_gen_lev_add}")  # first time we don't need check iterator < end_value

            # check iterator < end_value
            asm += gen_it_add
            asm.append(f"SWAP {reg_address}")
            asm.append(f"LOAD {reg_address}")  # load value of iterator to REGISTER a
            asm.append("INC a")  # iterator++
            asm.append(f"STORE {reg_address}")  # store iterator++
            asm.append(f"SWAP {reg_aux}")  # save iterator in REGISTER reg_aux

            asm += gen_lev_add
            asm.append(f"SWAP {reg_address}")
            asm.append(f"LOAD {reg_address}")  # load value of end_value to REGISTER a

            asm.append(f"SUB {reg_aux}")  # end_value - iterator
            asm.append(f"JNEG {len_commands_asm + 2}")  # omit loop, because iterator > end_value

            asm += commands_asm
            asm.append(f"JUMP -{9 + len_snippets}")

            del self.symbol_table[lev_name]

        if global_var:
            self.symbol_table[iterator_name] = global_var
        else:
            del self.symbol_table[iterator_name]

        return asm

    def for_downto(self, iterator_name, start_value_attr, end_value_attr, global_var, commands_asm):
        asm = []
        reg_aux = 'd'
        reg_address = 'h'

        iterator_address = self.symbol_table[iterator_name].address

        type1 = start_value_attr.value_type
        type2 = end_value_attr.value_type
        if type1 == "const" and type2 == "const":
            start_value = start_value_attr.value_content
            end_value = end_value_attr.value_content

            if start_value >= end_value:
                for i_value in range(start_value, end_value - 1, -1):
                    asm += self.generate_const(iterator_address)
                    asm.append(f"SWAP {reg_address}")
                    asm += self.generate_const(i_value)
                    asm.append(f"STORE {reg_address}")
                    asm += commands_asm

        else:
            pass
            if type1 == "var" and start_value_attr.value_content == iterator_name:
                raise Exception(f"Iterator {iterator_name} can't be as one of range of loop")
            if type2 == "var" and end_value_attr.value_content == iterator_name:
                raise Exception(f"Iterator {iterator_name} can't be as one of range of loop")

            len_commands_asm = len(commands_asm)

            gen_it_add = self.generate_const(iterator_address)
            len_gen_it_add = len(gen_it_add)

            lev_address, lev_name = self.symbol_table.loop_end_value_declaration()
            gen_lev_add = self.generate_const(lev_address)
            len_gen_lev_add = len(gen_lev_add)

            len_snippets = len_commands_asm + len_gen_it_add + len_gen_lev_add

            asm += start_value_attr.get_value_asm  # REGISTER a, b, h
            asm.append(f"SWAP {reg_address}")  # save start_value in REGISTER reg_address

            asm += gen_it_add  # generate address of iterator, REGISTER a, b
            asm.append(f"SWAP {reg_address}")  # start_value in REGISTER a, iterator_address in register reg_address
            asm.append(f"STORE {reg_address}")  # save start value of iterator
            asm.append(f"SWAP {reg_aux}")  # save start_value in REGISTER reg_aux

            asm += end_value_attr.get_value_asm  # REGISTER a, b, h
            asm.append(f"SWAP {reg_address}")  # save end_value in REGISTER reg_address

            asm += gen_lev_add
            asm.append(f"SWAP {reg_address}")  # lev_address in REGISTER reg_address, end_value in REGISTER a
            asm.append(f"STORE {reg_address}")  # save value of lev

            asm.append(f"SUB {reg_aux}")  # end_value - start_value

            asm.append(f"JPOS {11 + len_snippets}")  # omit loop, because start_value < end_value
            asm.append(f"JUMP {10 + len_gen_it_add + len_gen_lev_add}")  # first time we don't need check iterator < end_value

            # check iterator < end_value
            asm += gen_it_add
            asm.append(f"SWAP {reg_address}")
            asm.append(f"LOAD {reg_address}")  # load value of iterator to REGISTER a
            asm.append("DEC a")  # iterator--
            asm.append(f"STORE {reg_address}")  # store iterator--
            asm.append(f"SWAP {reg_aux}")  # save iterator in REGISTER reg_aux

            asm += gen_lev_add
            asm.append(f"SWAP {reg_address}")
            asm.append(f"LOAD {reg_address}")  # load value of end_value to REGISTER a

            asm.append(f"SUB {reg_aux}")  # end_value - iterator
            asm.append(f"JPOS {len_commands_asm + 2}")  # omit loop, because iterator > end_value

            asm += commands_asm
            asm.append(f"JUMP -{9 + len_snippets}")

            del self.symbol_table[lev_name]

        if global_var:
            self.symbol_table[iterator_name] = global_var
        else:
            del self.symbol_table[iterator_name]

        return asm
