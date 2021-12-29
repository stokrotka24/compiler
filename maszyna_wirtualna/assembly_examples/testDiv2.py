asm = []
asm.append("RESET c")
asm.append("DEC c")

asm.append("RESET d")
asm.append("INC d")

asm.append("RESET f")
asm.append("RESET g")

asm.append("GET")

asm.append("JZERO 57")
asm.append("JPOS 5")  # jeśli dzielnik jest niedodatni, obl. wart. bez.
asm.append("DEC g")
asm.append("SWAP e")
asm.append("RESET a")
asm.append("SUB e")

asm.append("SWAP e")  # w e wart. bez. dzielnika
asm.append("GET")

asm.append("JPOS 5")  # jeśli dzielna jest niedodatnia, obl. wart. bez.
asm.append("INC g")
asm.append("SWAP b")
asm.append("RESET a")
asm.append("SUB b")

asm.append("SWAP b")  # w b wart. bez. dzielnej

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
asm.append("JNEG 9")
asm.append("RESET a")
asm.append("INC a")
asm.append("SHIFT c")
asm.append("ADD f")
asm.append("SWAP f")
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
asm.append("JNEG -19")

asm.append("SWAP g")

asm.append("JZERO 5")
asm.append("INC f")
asm.append("RESET a")
asm.append("SUB f")
asm.append("JUMP 2")

asm.append("SWAP f")
asm.append("PUT")
asm.append("SWAP e")
asm.append("PUT")
asm.append("HALT")

asm = '\n'.join(asm)
print(asm)
