from enum import Enum
from typing import Dict

from InterpretError import InterpretErrorEnum, InterpretError
from Variable import Variable


class Frame:
    def __init__(self):
        self.variables: Dict[str, Variable] = {}

    def define_variable(self, name):
        if name in self.variables:
            raise InterpretError(InterpretErrorEnum.SEMANTIC_ERR, "Redefining variable " + name)
        self.variables[name] = Variable(name)

    def __str__(self):
        ret_str = "\n"
        for var in self.variables.values():
            ret_str += f"\tVariable {var.name}: {str(var.symbol_value)}\n"
        return ret_str