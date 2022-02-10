### Author: 
Hanna Stempniewicz

### Files description:

**Compiler.py** - main project file, parses given tokens and compiles input code to assembly language <br /> 
**CompilerLexer.py** - lexer <br /> 
**CodeGenerator.py** - includes auxiliary functions which translate parts of input code to assembly language <br /> 
**CompilerException.py** - an overridden exception, used to describe the exact location and cause of an error in the input code <br /> 
**ParserAttrs.py** - contains classes to store attributes for symbols <br /> 
**SymbolTable.py** - symbol table, stores information about variables, arrays, loop iterators for a given program <br /> 

### Requirements to launch the program (Ubuntu):
- python3.8.10
- SLY 0.4

### Launching program:
```
python3.8 Compiler.py <input_file> <output_file>
```

### Results
Compiler took 10th out of 65 places in compilers' ranking
