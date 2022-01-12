reg_counter = 'c'  # counter in PART_1, PART_2
reg_const = 'd'  # 1 in PART_1, -1 in PART_2
reg_dividend_flag = 'f' # 1 if dividend < 0, 0 otherwise
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

asm.append("GET")  # get dividend, REGISTER: a, b, h

asm.append(f"JZERO 70")  # -> END
asm.append("JPOS 5")  # no need set dividend flag
asm.append(f"INC {reg_dividend_flag}")  # set flag that dividend < 0
asm.append(f"SWAP {reg_dividend}")
asm.append("RESET a")
asm.append(f"SUB {reg_dividend}")

asm.append(f"SWAP {reg_dividend}")  # save |dividend|

asm.append("GET")  # get divisor, REGISTER: a, b, h

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
asm.append("PUT")

asm.append("HALT")
asm = '\n'.join(asm)
print(asm)