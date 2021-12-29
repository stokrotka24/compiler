asm = []
asm.append("RESET c")
asm.append("DEC c")

asm.append("RESET d")
asm.append("INC d")

asm.append("RESET f")  # 1 - dzielna ujemna
asm.append("RESET g")  # 1 - dzielnik ujemny

asm.append("GET")

asm.append(f"JZERO 75")
asm.append("JPOS 5")  # jeśli dzielnik jest niedodatni, obl. wart. bez.
asm.append("INC g")
asm.append("SWAP e")
asm.append("RESET a")
asm.append("SUB e")

asm.append("SWAP e")  # w e wart. bez. dzielnika
asm.append("GET")

asm.append("JZERO 67")
asm.append("JPOS 5")  # jeśli dzielna jest niedodatnia, obl. wart. bez.
asm.append("INC f")
asm.append("SWAP b")
asm.append("RESET a")
asm.append("SUB b")

asm.append("SWAP b")  # w b wart. bez. dzielnej
asm.append("RESET a")
asm.append("ADD e")
asm.append("SWAP h")  # w h wart. bez. dzielnika

asm.append("RESET a")  # dzielna mniejsza od dzielnika
asm.append("ADD e")
asm.append("SUB b")
asm.append("JPOS 2")
asm.append("JUMP 5")
asm.append("RESET a")
asm.append("ADD b")
asm.append("SWAP e")
asm.append("JUMP 32")

asm.append("JUMP 5")

asm.append("SWAP e")
asm.append("SHIFT d")
asm.append("INC c")
asm.append("SWAP e")

asm.append("RESET a")
asm.append("ADD e")
asm.append("SUB b")
asm.append("JNEG -7")
asm.append("JZERO -8")

asm.append("SWAP e")
asm.append("DEC d")
asm.append("DEC d")
asm.append("SHIFT d")  # podziel dzielnik przez 2
asm.append("SWAP b")
asm.append("SWAP e")  # zamień dzielną i dzielnik na miejsca

asm.append("RESET a")
asm.append("ADD e")
asm.append("SUB b")
asm.append("JNEG 4")
asm.append("SWAP e")
asm.append("SUB b")
asm.append("SWAP e")

asm.append("SWAP b")
asm.append("SHIFT d")
asm.append("SWAP b")
asm.append("DEC c")
asm.append("RESET a")
asm.append("DEC a")
asm.append("SUB c")
asm.append("JNEG -14")

asm.append("SWAP f")

asm.append("JZERO 9")
asm.append("SWAP g")
asm.append("JZERO 4")
asm.append("RESET a")  # CASE: dzielna ujemna, dzielnik ujemny
asm.append("SUB e")
asm.append("JUMP 11")
asm.append("SUB e")  # CASE: dzielna ujemna, dzielnik nieujemny
asm.append("ADD h")
asm.append("JUMP 8")
asm.append("SWAP g")
asm.append("JZERO 5")
asm.append("RESET a")  # CASE: dzielna nieujemna, dzielnik ujemny
asm.append("ADD e")
asm.append("SUB h")
asm.append("JUMP 2")
asm.append("SWAP e")  # CASE: dzielna nieujemna, dzielnik nieujemny
asm.append("PUT")
asm.append("HALT")
asm = '\n'.join(asm)
print(asm)
