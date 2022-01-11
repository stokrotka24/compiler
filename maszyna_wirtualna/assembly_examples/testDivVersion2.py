# X DIV Y
asm = []
asm.append("RESET c")
asm.append("DEC c")  # -1 do 1. części algorytmu

asm.append("RESET d")
asm.append("INC d")  # 1 do shiftów

asm.append("RESET f")
asm.append("RESET g")  # flaga, czy należy zmienić wynik

asm.append("GET")  # wczytaj X

asm.append(f"JZERO 66")  # TODO skok do KONIEC
asm.append("JPOS 5")  # nie ustawiaj flagi
asm.append("DEC g")  # ustaw flagę, że X < 0
asm.append("SWAP e")
asm.append("RESET a")
asm.append("SUB e")

asm.append("SWAP e")  # zapisz w REGISTER e: |X|

asm.append("GET")  # wczytaj Y

asm.append("JZERO 58")  # TODO skok do KONIEC
asm.append("JPOS 5")  # nie ustawiaj flagi
asm.append("INC g")  # ustaw flagę, że Y < 0
asm.append("SWAP b")
asm.append("RESET a")
asm.append("SUB b")

asm.append("SWAP b")  # zapisz w REGISTER b: |Y|

asm.append("RESET a")
asm.append("ADD b")
asm.append("SUB e")
asm.append("JPOS 2")  # TODO |X| < |Y|
asm.append("JUMP 3")  # TODO |X| >= |Y|
asm.append("RESET a")
asm.append("JUMP 33")  # TODO |X| < |Y|, skocz do CHANGE_RESULT

# LOOP_1
asm.append("ADD b")
asm.append("SWAP b")
asm.append("SHIFT d")
asm.append("INC c")

asm.append("SWAP b")
asm.append("JPOS 2")
asm.append("JUMP -6")  # TODO Y <= X, więc nie wychodzimy LOOP_1

asm.append("RESET d")
asm.append("DEC d")  # -1 do dzielenia przez 2

asm.append("SWAP b")
asm.append("SHIFT d")  # Y // 2
asm.append("SWAP b")  # REGISTER b: Y

# LOOP_2
asm.append("RESET a")
asm.append("ADD e")
asm.append("SUB b")
asm.append("JNEG 7")  # TODO X < Y, więc skocz do SKIP
asm.append("SWAP e")  # X = X - Y
asm.append("RESET a")  # w REGISTER a, mieliśmy starą wartość X, już nam się nie przyda
asm.append("INC a")
asm.append("SHIFT c")
asm.append("ADD f")
asm.append("SWAP f")  # REGISTER f: f + 2^c

# SKIP
asm.append("SWAP b")
asm.append("SHIFT d")  # Y // 2
asm.append("SWAP b")  # REGISTER b: Y

asm.append("DEC c")
asm.append("RESET a")
asm.append("DEC a")
asm.append("SUB c")
asm.append("JNEG -17")  # REGISTER c =/= -1, więc wróć do LOOP_2

asm.append("SWAP e")
asm.append("JZERO 7")  # TODO reszta = 0, skocz do EXCEPTION_CHANGE_RESULT

# CHANGE_RESULT
asm.append("SWAP g")
asm.append("JZERO 10")  # TODO nie trzeba zmieniać wyniku
asm.append("RESET a")
asm.append("SUB f")
asm.append("DEC a")
asm.append("JUMP 7")  # TODO, skocz do KONIEC

# EXCEPTION_CHANGE_RESULT
asm.append("SWAP g")
asm.append("JZERO 4")  # TODO nie trzeba zmieniać wyniku
asm.append("RESET a")
asm.append("SUB f")
asm.append("JUMP 2")  # TODO, skocz do KONIEC

asm.append("SWAP f")

# KONIEC
asm.append("PUT")

asm.append("HALT")
asm = '\n'.join(asm)
print(asm)