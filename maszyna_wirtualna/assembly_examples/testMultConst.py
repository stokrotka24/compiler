import testGenConst

number1 = 3000
number2 = -50000
asm = ""
if number1 == 0 or number2 == 0:
    asm += "RESET a\n"
else:
    # in register r_a is number1
    asm += testGenConst.generateConstant(abs(number1))
    asm += "RESET h\n"
    asm += "STORE h\n"
    asm += "RESET b\n"
    asm += "RESET c\n"
    binary = f'{abs(number2):b}'
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
                asm += "LOAD h\n"
                asm += "SHIFT c\n"
                asm += "ADD b\n"
        asm += "INC c\n"
    if number1 * number2 < 0:
        asm += "SWAP b\n"
        asm += "RESET a\n"
        asm += "SUB b\n"
asm += "PUT\n"
asm += "HALT\n"
print(asm)

# dodać ify gdy mnożymy przez 1, -1?
