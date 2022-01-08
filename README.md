###Autor: 
Hanna Stempniewicz

###Zawartość plików:

**kompilator.py** - główny plik projektu, parsuje dostarczone tokeny i kompiluje kod wejściowy na kod asemblerowy <br /> 
**CompilerLexer.py** - lekser <br /> 
**CodeGenerator.py** - zawiera funkcje pomocnicze do przekładu kodu wejściowego na kod asemblerowy <br /> 
**CompilerException.py** - nadpisany wyjątek, służący do dokładnego opisania miejsca i przyczyny błędu w kodzie wejściowym <br /> 
**ParserAttrs.py** - zawiera klasy pomocnicze do przechowywania atrybutów dla symboli <br /> 
**SymbolTable.py** - tablica symboli, przechowująca informacje o zmiennych, tablicach, iteratorach pętli dla danego programu <br /> 

###Wymagania do uruchomienia programu (dla systemu Ubuntu):
- python3.8.10
- SLY 0.4

###Uruchomienie programu:
```
python3.8 kompilator.py <nazwa pliku wejściowego> <nazwa pliku wyjściowego>
```
