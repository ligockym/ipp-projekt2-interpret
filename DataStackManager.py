from Instruction import Instruction
from Symbol import SymbolType, SymbolTypeHelper
from Variable import Variable


class DataStackManager:
    def __init__(self, interpret):
        self.interpret = interpret

    def pushs(self, instruction: Instruction):
        instruction.check_format([SymbolTypeHelper.DATABLE_NIL])
        arg = instruction.args.get(1)
        real_symbol = self.interpret.memory.symbol_or_var_symbol(arg)
        self.interpret.memory.push_data_stack(real_symbol)

    def pops(self, instruction: Instruction):
        instruction.check_format([[SymbolType.VAR]])

        var = instruction.args.get(1)
        var_from_memory: Variable = self.interpret.memory.get_variable(var.value, var.frame)
        var_from_memory.symbol_value = self.interpret.memory.pop_data_stack()
