class Variable:
    def __init__(self, address, loop_iterator):
        self.address = address
        self.loop_iterator = loop_iterator
        self.initialized = False

    def __repr__(self):
        return f"<Variable: address: {self.address}, loop_iterator: {self.loop_iterator}, " \
               f"initialized: {self.initialized}>"


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
        self.loop_end_values = 0

    def __repr__(self) -> str:
        return "<SymbolTable: " + super().__repr__() + ">"

    def loop_iterator_declaration(self, name):
        self[name] = Variable(self.data_offset, True)
        self.data_offset += 1

    def loop_end_value_declaration(self):
        lev_name = f"lev_{self.loop_end_values}"
        self.loop_end_values += 1

        self[lev_name] = Variable(self.data_offset, False)
        self.data_offset += 1

        return self.data_offset - 1, lev_name

    def variable_declaration(self, name):
        if name in self:
            return f"Variable {name} already declared"
        self[name] = Variable(self.data_offset, False)
        self.data_offset += 1

    def array_declaration(self, name, first_index, last_index):
        if name in self:
            return f"Array {name} already declared"
        if first_index > last_index:
            return f"First index of array {name} can't be greater then last index of array"
        self[name] = Array(self.data_offset, first_index, last_index)
        self.data_offset += last_index - first_index + 1
