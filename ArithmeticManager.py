from typing import Dict

from Instruction import Instruction
from InterpretError import InterpretErrorEnum, InterpretError
from Symbol import SymbolType, SymbolTypeHelper, Symbol
from Variable import Variable


class ArithmeticManager:
    def __init__(self, interpret):
        self.interpret = interpret

    def add(self, instruction: Instruction):
        var, symb1, symb2 = self._add_sub_mul_idiv(instruction)
        var.symbol_value.value = symb1.value + symb2.value

    def sub(self, instruction: Instruction):
        var, symb1, symb2 = self._add_sub_mul_idiv(instruction)
        var.symbol_value.value = symb1.value - symb2.value

    def mul(self, instruction: Instruction):
        var, symb1, symb2 = self._add_sub_mul_idiv(instruction)
        var.symbol_value.value = symb1.value * symb2.value

    def idiv(self, instruction: Instruction):
        var, symb1, symb2 = self._add_sub_mul_idiv(instruction)
        if symb2.value == 0:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_VALUE, "Division by zero")
        var.symbol_value.value = symb1.value // symb2.value

    def lt(self, instruction: Instruction):
        var, symb1, symb2 = self._lt_gt_eq(instruction)
        self._check_if_same(symb1, symb2)
        if symb1.type == SymbolType.NIL:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE, "Cannot compare with nil")
        var.symbol_value.value = symb1.value < symb2.value

    def gt(self, instruction: Instruction):
        var, symb1, symb2 = self._lt_gt_eq(instruction)
        self._check_if_same(symb1, symb2)
        if symb1.type == SymbolType.NIL:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE, "Cannot compare with nil")
        var.symbol_value.value = symb1.value > symb2.value

    def eq(self, instruction: Instruction):
        var, symb1, symb2 = self._lt_gt_eq(instruction)

        # if both symbols are non-nil, they have to be the same type
        if symb1.type != SymbolType.NIL and symb2.type != SymbolType.NIL:
            self._check_if_same(symb1, symb2)
            var.symbol_value.value = symb1.value == symb2.value
        else:
            # at least one of symbols is nil -> compare types
            var.symbol_value.value = symb1.type == symb2.type

    def and_fn(self, instruction: Instruction):
        var, symb1, symb2 = self._and_or(instruction)
        var.symbol_value.value = symb1.value and symb2.value

    def or_fn(self, instruction: Instruction):
        var, symb1, symb2 = self._and_or(instruction)
        var.symbol_value.value = symb1.value or symb2.value

    def not_fn(self, instruction: Instruction):
        instruction.check_format([[SymbolType.VAR], SymbolTypeHelper.DATABLE_NIL])

        symb_var: Symbol = instruction.args.get(1)
        symb1: Symbol = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(2))
        var: Variable = self.interpret.memory.get_variable(symb_var.value, symb_var.frame)

        if symb1.type != SymbolType.BOOL:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE, "Not can be used only with bool")

        var.symbol_value.value = not symb1.value
        var.symbol_value.type = SymbolType.BOOL

    def int2char(self, instruction: Instruction):
        instruction.check_format([[SymbolType.VAR], [SymbolType.VAR, SymbolType.INT]])
        symb_var: Symbol = instruction.args.get(1)
        symb1: Symbol = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(2))
        if symb1.type != SymbolType.INT:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE, "Int2Char requires integer")
        var: Variable = self.interpret.memory.get_variable(symb_var.value, symb_var.frame)

        try:
            var.symbol_value.value = chr(symb1.value)
            var.symbol_value.type = SymbolType.STRING

        except ValueError:
            raise InterpretError(InterpretErrorEnum.WRONG_STRING_OPERATION)

    def stri2int(self, instruction: Instruction):
        var, symb1, symb2 = self._parse_args(instruction)
        if symb1.type != SymbolType.STRING or symb2.type != SymbolType.INT:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE)

        if symb2.value < 0:
            raise InterpretError(InterpretErrorEnum.WRONG_STRING_OPERATION)

        try:
            var.symbol_value.value = ord(symb1.value[symb2.value])
            var.symbol_value.type = SymbolType.INT
        except (IndexError, ValueError):
            raise InterpretError(InterpretErrorEnum.WRONG_STRING_OPERATION, "Wrong indexing of stri2int")

    def _lt_gt_eq(self, instruction: Instruction):
        var, symb1, symb2 = self._parse_args(instruction)
        var.symbol_value.type = SymbolType.BOOL
        return var, symb1, symb2

    def _and_or(self, instruction: Instruction):
        var, symb1, symb2 = self._parse_args(instruction)
        if symb1.type != SymbolType.BOOL or symb2.type != SymbolType.BOOL:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE, "And/Or can be used only with bools")
        var.symbol_value.type = SymbolType.BOOL
        return var, symb1, symb2

    def _add_sub_mul_idiv(self, instruction: Instruction):
        var, symb1, symb2 = self._parse_args(instruction)

        # check if symb1 and symb2 are both type of int
        if symb1.type != SymbolType.INT or symb2.type != SymbolType.INT:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE, "Add/Sub/Mul/IDiv argument is not int")

        var.symbol_value.type = SymbolType.INT
        return var, symb1, symb2

    def _parse_args(self, instruction: Instruction):
        instruction.check_format([[SymbolType.VAR], SymbolTypeHelper.DATABLE_NIL, SymbolTypeHelper.DATABLE_NIL])
        symb_var: Symbol = instruction.args.get(1)
        symb1: Symbol = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(2))
        symb2: Symbol = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(3))

        var: Variable = self.interpret.memory.get_variable(symb_var.value, symb_var.frame)
        return var, symb1, symb2

    def _check_if_same(self, symb1, symb2):
        if symb1.type != symb2.type:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE, "Type of symbol 1 is not equal to the type of symbol 2")