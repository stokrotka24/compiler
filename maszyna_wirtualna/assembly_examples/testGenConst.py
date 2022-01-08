# WOLNIEJSZY SPOSÓB
# number = 97
# asm = ""
#
# binary = f'{number:b}'
# n = len(binary)
# asm += "RESET a\n"
# asm += "RESET b\n"
# asm += "RESET c\n"
# for i in range(n - 1, -1, -1):
#     if binary[i] == '1':
#         asm += "SWAP b\n"
#         asm += "RESET a\n"
#         asm += "INC a\n"
#         asm += "SHIFT c\n"
#         asm += "ADD b\n"
#     asm += "INC c\n"
# asm += "PUT \n"
# asm += "HALT \n"
# print(asm)

def generateConstant(number=0):
    asm = ""
    instr = "INC" if number >= 0 else "DEC"

    binary = f'{abs(number):b}'
    asm += "RESET a\n"
    asm += "RESET b\n"
    asm += "INC b\n"
    for bit in binary[:-1]:
        if bit == '1':
            asm += f"{instr} a\n"
        asm += "SHIFT b\n"
    if binary[-1] == '1':
        asm += f"{instr} a\n"
    asm += "PUT \n"
    return asm


# Zastanowić, się czy wybór rejestru b jako rejestru pomocniczego jest dobrym wyborem

if __name__ == '__main__':
    asm_code = generateConstant(-9223372036854775808)
    asm_code += "HALT \n"
    print(asm_code)
