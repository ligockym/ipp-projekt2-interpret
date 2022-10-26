from Instruction import Instruction
from InterpretError import InterpretErrorEnum, InterpretError
from Symbol import SymbolType, SymbolTypeHelper
from Variable import Variable


class FrameFuncManager:
    def __init__(self, interpret):
        self.interpret = interpret

    def move(self, instruction: Instruction):
        instruction.check_format([[SymbolType.VAR], SymbolTypeHelper.DATABLE_NIL])
        move_to = instruction.args.get(1)
        move_from = instruction.args.get(2)

        move_to_var: Variable = self.interpret.memory.get_variable(move_to.value, move_to.frame)
        move_from = self.interpret.memory.symbol_or_var_symbol(move_from)

        move_to_var.symbol_value = move_from

    def create_frame(self, instruction: Instruction):
        instruction.check_format([])
        self.interpret.memory.new_temp_frame()

    def push_frame(self, instruction: Instruction):
        instruction.check_format([])
        self.interpret.memory.push_temp_to_local()

    def pop_frame(self, instruction: Instruction):
        instruction.check_format([])
        self.interpret.memory.pop_local_to_temp()

    def defvar(self, instruction: Instruction):
        instruction.check_format([[SymbolType.VAR]])
        var_arg = instruction.args.get(1)
        self.interpret.memory.def_variable(var_arg.value, var_arg.frame)

    def call(self, instruction: Instruction):
        instruction.check_format([[SymbolType.LABEL]])

        label_name = instruction.args.get(1).value

        self.interpret.push_counter()
        self.interpret.jump_label(label_name)

    def return_fn(self, instruction: Instruction):
        instruction.check_format([])
        self.interpret.pop_counter()











