class InterpretErrorEnum:
    ARG_ERR = 1
    TO_BE_DONE=2
    WRONG_XML_FORMAT=31
    UNEXPECTED_XML=32
    SEMANTIC_ERR=52
    WRONG_OPERAND_TYPE= 53,
    NON_EXISTING_VAR=54,
    NON_EXISTING_FRAME=55,
    NON_EXISTING_VALUE=56,
    WRONG_OPERAND_VALUE=57, # TODO: Check if 57 or 53 is correct for all usages
    WRONG_STRING_OPERATION=58


class InterpretError(Exception):
    def __init__(self, error_type: InterpretErrorEnum, error_message: str = ''):
        self.error_type = error_type
        self.error_message = error_message
        super().__init__(self.error_message)

    def __str__(self):
        return f'{self.error_type} -> {self.error_message}'
