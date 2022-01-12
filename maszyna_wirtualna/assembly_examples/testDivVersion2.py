reg_counter = 'c'  # counter in PART_1, PART_2
reg_const = 'd'  # 1 in PART_1, -1 in PART_2
reg_quotient = 'f'
reg_flag = 'g'  # 0, if there is no need change quotient
reg_dividend = 'e' # =/= a, b, h, because they are used to load divisor
reg_divisor = 'b'

asm = []
asm.append(f"RESET {reg_counter}")
asm.append(f"DEC {reg_counter}")

asm.append(f"RESET {reg_const}")
asm.append(f"INC {reg_const}")

asm.append(f"RESET {reg_quotient}")
asm.append(f"RESET {reg_flag}")

asm.append("GET")  # get dividend, REGISTER: a, b, h

asm.append(f"JZERO 66")  # -> END
asm.append("JPOS 5")  # no need set flag
asm.append(f"DEC {reg_flag}")  # set flag that dividend < 0
asm.append(f"SWAP {reg_dividend}")
asm.append("RESET a")
asm.append(f"SUB {reg_dividend}")

asm.append(f"SWAP {reg_dividend}")  # save dividend

asm.append("GET")  # get divisor, REGISTER: a, b, h

asm.append("JZERO 58")  # -> END
asm.append("JPOS 5")  # no need set flag
asm.append(f"INC {reg_flag}")  # set flag that divisor < 0
asm.append(f"SWAP {reg_divisor}")
asm.append("RESET a")
asm.append(f"SUB {reg_divisor}")

asm.append(f"SWAP {reg_divisor}")  # save divisor

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

asm.append(f"SWAP {reg_dividend}") # rest
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
asm.append("PUT")

asm.append("HALT")
asm = '\n'.join(asm)
print(asm)