from Instruction import Instruction
from InterpretError import InterpretErrorEnum, InterpretError
from Symbol import SymbolType, Symbol
from Variable import Variable


class StringManager:
    def __init__(self, interpret):
        self.interpret = interpret

    def concat(self, instruction: Instruction):
        instruction.check_format(
            [[SymbolType.VAR], [SymbolType.VAR, SymbolType.STRING], [SymbolType.VAR, SymbolType.STRING]])

        symb_var = instruction.args.get(1)
        symb1: Symbol = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(2))
        symb2: Symbol = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(3))

        if symb1.type != SymbolType.STRING or symb2.type != SymbolType.STRING:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE, "Both symbols have to be strings.")

        var: Variable = self.interpret.memory.get_variable(symb_var.value, symb_var.frame)
        var.symbol_value.value = symb1.value + symb2.value
        var.symbol_value.type = SymbolType.STRING

    def strlen(self, instruction: Instruction):
        instruction.check_format([[SymbolType.VAR], [SymbolType.VAR, SymbolType.STRING]])

        symb_var = instruction.args.get(1)
        symb1: Symbol = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(2))

        if symb1.type != SymbolType.STRING:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE, "Symbol has to be strings.")

        var: Variable = self.interpret.memory.get_variable(symb_var.value, symb_var.frame)
        var.symbol_value.value = len(symb1.value)
        var.symbol_value.type = SymbolType.INT

    def getchar(self, instruction: Instruction):
        instruction.check_format(
            [[SymbolType.VAR], [SymbolType.VAR, SymbolType.STRING], [SymbolType.VAR, SymbolType.INT]])

        symb_var = instruction.args.get(1)
        symb1: Symbol = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(2))
        symb2: Symbol = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(3))

        # check correct types of symbols
        if symb1.type != SymbolType.STRING or symb2.type != SymbolType.INT:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE, "Wrong operand types for getchar")

        # check if indexing is not negative
        if symb2.value < 0:
            raise InterpretError(InterpretErrorEnum.WRONG_STRING_OPERATION, "Wrong indexing in getchar")

        var: Variable = self.interpret.memory.get_variable(symb_var.value, symb_var.frame)
        try:
            var.symbol_value.value = symb1.value[symb2.value]
            var.symbol_value.type = SymbolType.STRING
        except Exception:
            raise InterpretError(InterpretErrorEnum.WRONG_STRING_OPERATION, "Wrong indexing in getchar")

    def setchar(self, instruction: Instruction):
        instruction.check_format(
            [[SymbolType.VAR], [SymbolType.VAR, SymbolType.INT], [SymbolType.VAR, SymbolType.STRING]])

        symb_var = instruction.args.get(1)
        symb1: Symbol = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(2))
        symb2: Symbol = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(3))
        var: Variable = self.interpret.memory.get_variable(symb_var.value, symb_var.frame)

        # check if variable is initialized
        self.interpret.memory.symbol_or_var_symbol(symb_var)

        if symb1.type != SymbolType.INT or symb2.type != SymbolType.STRING or var.symbol_value.type != SymbolType.STRING:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE, "Wrong operand values for setchar")

        # check if indexing is not negative
        if symb1.value < 0:
            raise InterpretError(InterpretErrorEnum.WRONG_STRING_OPERATION, "Wrong indexing in setchar")

        try:
            var.symbol_value.value = self._replace_string(var.symbol_value.value, symb1.value, symb2.value[0])
            var.symbol_value.type = SymbolType.STRING
        except:
            raise InterpretError(InterpretErrorEnum.WRONG_STRING_OPERATION, "Wrong indexing in setchar")

    def _replace_string(self, s: str, index: int, replace_with: str) -> str:
        if index >= len(s):
            raise InterpretError(InterpretErrorEnum.WRONG_STRING_OPERATION)
        return s[:index] + replace_with + s[index + 1:]
