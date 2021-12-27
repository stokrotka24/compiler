class IdentifierAttr:
    def __init__(self, var_address_asm, var_name):
        self.var_address_asm = var_address_asm
        self.var_name = var_name


class ValueAttr:
    def __init__(self, get_value_asm, value_type, value_content):
        self.get_value_asm = get_value_asm
        self.value_type = value_type
        self.value_content = value_content
