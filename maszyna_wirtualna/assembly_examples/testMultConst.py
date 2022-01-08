# a * b:
# a,b stałe - wstaw do rejestru wynikowego a * b
# a,b, jedna zmienna, jedna stała - użyj sposobu z tego pliku i po asemblerowych obliczeniach w rejestrze wynikowym bedzie a * b
# przy czym pamiętaj zamienić tak, aby na drugim miejcu była stała, a do rejestru a załaduj wartość zmiennej
# to się opłaca tylko wtedy gdy stała jest mniejsza od wartości zmiennej

import testGenConst

const = 30
asm = ""
if const == 0:
    asm += "RESET a\n"
else:
    # asm += testGenConst.generateConstant(abs(number1)) - for test generate const,
    # in practice we have value of variable in r_a
    instr = "ADD" if const >= 0 else "SUB"
    asm += "GET\n"
    asm += "SWAP d\n"  # value of number1 saved in register d
    asm += "RESET a\n"
    asm += f"{instr} d\n"
    asm += "RESET b\n"
    asm += "RESET c\n"
    binary = f'{abs(const):b}'
    n = len(binary)
    first_one_read = False
    for i in range(n - 1, -1, -1):
        if binary[i] == '1':
            if not first_one_read:
                first_one_read = True
                if i != n - 1:
                    asm += "SHIFT c\n"
            else:
                asm += "SWAP b\n"
                asm += "RESET a\n"
                asm += f"{instr} d\n"
                asm += "SHIFT c\n"
                asm += "ADD b\n"
        asm += "INC c\n"
asm += "PUT\n"
asm += "HALT\n"
print(asm)

# dodać ify gdy mnożymy przez 1, -1?
# dodać shift gdy mnożymy przez 2?
