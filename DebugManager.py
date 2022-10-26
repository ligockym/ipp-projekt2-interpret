import sys

from Instruction import Instruction
from Symbol import SymbolTypeHelper


class DebugManager:
    def __init__(self, interpret):
        self.interpret = interpret

    def dprint(self, instruction: Instruction):
        instruction.check_format([SymbolTypeHelper.DATABLE_NIL])
        symb = self.interpret.memory.symbol_or_var_symbol(instruction.args.get(1))
        print(symb, file=sys.stderr)

    def break_fn(self, instruction: Instruction):
        instruction.check_format([])

        print(self.interpret, file=sys.stderr)