asm = []
# najpierw wczytujemy dzielnik
asm.append("RESET f")
asm.append("GET")
asm.append("SWAP e")  # w e zapamiętujemy dzielnik
asm.append("GET")
asm.append("SWAP b")
# w b mamy dzielną, w e mamy dzielnik

asm.append("RESET c")
asm.append("DEC c")  # -1 w c

asm.append("RESET d")
asm.append("INC d")  # 1 w d do mnozenia przez 2

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

asm.append("SWAP f")
asm.append("PUT")
asm.append("SWAP e")
asm.append("PUT")
asm.append("HALT")

# asm.append("PUT") # 11
# asm.append("SWAP b") # 24
# asm.append("PUT")
# asm.append("SWAP c") # 3
# asm.append("PUT")
# asm.append("SWAP d") # -1
# asm.append("PUT")
# asm.append("SWAP e") # 37
# asm.append("PUT")
# asm.append("SWAP f") # 0
# asm.append("PUT")
asm.append("HALT")

asm = '\n'.join(asm)
print(asm)
