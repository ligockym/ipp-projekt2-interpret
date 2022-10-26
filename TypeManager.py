from Instruction import Instruction
from Symbol import SymbolType, SymbolTypeHelper
from Variable import Variable


class TypeManager:
    def __init__(self, interpret):
        self.interpret = interpret

    def type(self, instruction: Instruction):
        instruction.check_format([[SymbolType.VAR], SymbolTypeHelper.DATABLE_NIL])
        symb_var = instruction.args.get(1)
        symb1 = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(2), False)
        var: Variable = self.interpret.memory.get_variable(symb_var.value, symb_var.frame)

        var.symbol_value.value = symb1.type_to_str()
        var.symbol_value.type = SymbolType.STRING