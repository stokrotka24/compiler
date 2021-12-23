asm = ""
asm += "RESET g\n"  # jeżeli jest równy 0, to nie bedziemy zmieniac znaku mnozenia
asm += "GET\n"  # wczytanie 1. zmiennej

asm += "JPOS 5\n"

# wartość bezwzględna 1.zmiennej, jeśli jest niedodatnia
asm += "DEC g\n"
asm += "SWAP b\n"
asm += "RESET a\n"
asm += "SUB b\n"

asm += "SWAP b\n"  # zapisanie 1. zmiennej w rejestrze b

asm += "GET\n"  # wczytanie 2. zmiennej

asm += "JPOS 5\n"

# wartość bezwzględna 2.zmiennej, jeśli jest ujemna
asm += "INC g\n"
asm += "SWAP c\n"
asm += "RESET a\n"
asm += "SUB c\n"

asm += "SWAP c\n"  # zapisanie 2. zmiennej w rejestrze b

# sprawdzenie, która liczba ma mniejszą wartość bezwzględną
asm += "RESET a\n"
asm += "ADD c\n"
asm += "SUB b\n"
asm += "JNEG 6\n"
asm += "SWAP c\n"
asm += "SWAP d\n"
asm += "RESET a\n"
asm += "ADD b\n"
asm += "JUMP 5\n"
asm += "SWAP b\n"
asm += "SWAP d\n"
asm += "RESET a\n"
asm += "ADD c\n"
# teraz w rejestrze a mamy większą liczbę z 2 wczytanych
asm += "RESET c\n"
asm += "DEC c\n"  # -1 do dzielenia przez 2
asm += "RESET e\n"  # wykladnik potęgi
asm += "RESET f\n"  # aktualny wynik mnożenia

asm += "SWAP b\n"
asm += "RESET a\n"
asm += "ADD b\n"
asm += "SHIFT c\n"
asm += "SWAP b\n"
asm += "SUB b\n"
asm += "SUB b\n"

asm += "JZERO 8\n"

asm += "RESET a\n"
asm += "ADD d\n"
asm += "SHIFT e\n"  # mnożymy przez odpowiednią potęgę dwójki
asm += "ADD f\n"  # dodajemy poprzedni wynik
asm += "SWAP f\n"
asm += "RESET a\n"
asm += "INC a\n"

asm += "INC e\n"
asm += "SWAP b\n"
asm += "JPOS -17"
asm += "SWAP g\n"

asm += "JZERO 6\n"

# zmienianie znaku wyniku na ujemny
asm += "SWAP f\n"
asm += "SWAP b\n"
asm += "RESET a\n"
asm += "SUB b\n"
asm += "JUMP 2\n"
asm += "SWAP f\n"
asm += "PUT\n"
asm += "HALT\n"
print(asm)
