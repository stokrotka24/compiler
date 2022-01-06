class IdentifierAttr:
    def __init__(self, identifier_address_asm, identifier_type, identifier_name):
        self.identifier_address_asm = identifier_address_asm
        self.identifier_type = identifier_type
        self.identifier_name = identifier_name


class ValueAttr:
    def __init__(self, get_value_asm, value_type, value_content):
        self.get_value_asm = get_value_asm
        self.value_type = value_type
        self.value_content = value_content  # number if value_type is "const", variable/array name if "var", "arr"


class ConditionAttr:
    def __init__(self, get_difference_asm, condition_type):
        self.get_difference_asm = get_difference_asm
        self.condition_type = condition_type
