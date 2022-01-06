class Variable:
    def __init__(self, address):
        self.address = address
        self.initialized = False

    def __repr__(self):
        return f"<Variable: address: {self.address}, initialized: {self.initialized}>"


class Array:
    def __init__(self, address, first_index, last_index):
        self.address = address
        self.first_index = first_index
        self.last_index = last_index
        self.initialized = []  # indexes of initialized elements

    def __repr__(self):
        return f"<Array: address: {self.address}, first_index: {self.first_index}, " \
               f"last_index: {self.last_index}, initialized: {self.initialized}>"


class SymbolTable(dict):
    def __init__(self):
        super().__init__()
        self.data_offset = 0

    def __repr__(self) -> str:
        return "<SymbolTable: " + super().__repr__() + ">"

    def variable_declaration(self, name):
        if name in self:
            return f"Variable {name} already declared"
        self[name] = Variable(self.data_offset)
        self.data_offset += 1

    def array_declaration(self, name, first_index, last_index):
        if name in self:
            return f"Array {name} already declared"
        if first_index > last_index:
            return f"First index of array can't be greater then last index of array"
        self[name] = Array(self.data_offset, first_index, last_index)
        self.data_offset += last_index - first_index + 1
