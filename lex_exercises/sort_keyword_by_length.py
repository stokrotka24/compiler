strs = ["VAR", "BEGIN", "END",
        "ASSIGN",
        "IF", "THEN", "ELSE", "ENDIF",
        "WHILE", "DO", "ENDWHILE",
        "REPEAT", "UNTIL",
        "FOR", "FROM", "TO", "DOWNTO", "ENDFOR",
        "READ", "WRITE",
        "PLUS", "MINUS", "TIMES", "DIV", "MOD",
        "EQ", "NEQ", "LE", "GE", "LEQ", "GEQ",
        "NUM", "PIDENTIFIER"]
print(sorted(strs, key=len, reverse=True))