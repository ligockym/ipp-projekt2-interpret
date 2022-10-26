import sys

from Instruction import Instruction
from InterpretError import InterpretErrorEnum, InterpretError
from Symbol import SymbolType, SymbolTypeHelper, Symbol


class JumpManager:
    def __init__(self, interpret):
        self.interpret = interpret

    def label(self, instruction: Instruction):
        instruction.check_format([[SymbolType.LABEL]])
        label_name = instruction.args.get(1).value
        label_counter = instruction.order

        self.interpret.save_label(label_name, label_counter)

    def jump(self, instruction: Instruction):
        instruction.check_format([[SymbolType.LABEL]])
        label_name = instruction.args.get(1).value

        self.interpret.jump_label(label_name)

    def jumpifeq(self, instruction: Instruction):
        instruction.check_format([[SymbolType.LABEL], SymbolTypeHelper.DATABLE_NIL, SymbolTypeHelper.DATABLE_NIL])

        label_name = instruction.args.get(1).value
        symb1: Symbol = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(2))
        symb2: Symbol = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(3))

        self.interpret.does_label_exist(label_name)

        at_least_one_nil = symb1.type == SymbolType.NIL or symb2.type == SymbolType.NIL
        if (symb1.type != symb2.type) and not at_least_one_nil:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE, "Wrong operand type")

        if (at_least_one_nil and symb1.type == symb2.type) or (symb1.value == symb2.value):
            self.interpret.jump_label(label_name)

    def jumpifneq(self, instruction: Instruction):
        instruction.check_format([[SymbolType.LABEL], SymbolTypeHelper.DATABLE_NIL, SymbolTypeHelper.DATABLE_NIL])

        label_name = instruction.args.get(1).value
        symb1: Symbol = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(2))
        symb2: Symbol = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(3))

        self.interpret.does_label_exist(label_name)

        at_least_one_nil = symb1.type == SymbolType.NIL or symb2.type == SymbolType.NIL
        if (symb1.type != symb2.type) and not at_least_one_nil:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE, "Wrong operand type")

        if (at_least_one_nil and symb1.type == symb2.type) or (symb1.value == symb2.value):
            return
        self.interpret.jump_label(label_name)

    def exit(self, instruction: Instruction):
        instruction.check_format([[SymbolType.INT, SymbolType.VAR]])

        symb:Symbol = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(1))
        if symb.type != SymbolType.INT:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE)
        elif not (0 <= symb.value <= 49):
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_VALUE)

        sys.exit(symb.value)