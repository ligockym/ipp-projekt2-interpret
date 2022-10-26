import sys

from Instruction import Instruction
from InterpretError import InterpretError, InterpretErrorEnum
from Symbol import SymbolTypeHelper, Symbol, SymbolType
from Variable import Variable


class IOManager:
    def __init__(self, interpret):
        self.interpret = interpret

    def write(self, instruction: Instruction):
        # only one parameter of any datable type
        instruction.check_format([SymbolTypeHelper.DATABLE_NIL])
        to_write = instruction.args.get(1)

        symbol_to_write: Symbol = self.interpret.memory.symbol_or_var_symbol(to_write)
        print(symbol_to_write.to_str(), end='')

    def read(self, instruction: Instruction):
        instruction.check_format([[SymbolType.VAR], [SymbolType.TYPE]])
        var_symb: Symbol = instruction.args.get(1)
        type_symb: Symbol = instruction.args.get(2)
        read_type: SymbolType = type_symb.value

        input_value = self.interpret.input_one_value()
        if input_value is None:
            value = Symbol(SymbolType.NIL, 'nil')
        else:
            try:
                value = Symbol(read_type, input_value)  # conversion is done in symbol

            except InterpretError as err:
                # error in Symbol creation -> wrong type so use NIL
                if err.error_type == InterpretErrorEnum.UNEXPECTED_XML:
                    value = Symbol(SymbolType.NIL, 'nil')

        var: Variable = self.interpret.memory.get_variable(var_symb.value, var_symb.frame)
        var.symbol_value = value
