from typing import List, Dict

from InterpretError import InterpretErrorEnum, InterpretError
from Symbol import Symbol, SymbolType


class Instruction:
    def __init__(self, opcode: str, order: int, args: Dict[int, Symbol]):
        self.opcode = opcode.upper()
        self.order = order
        self.args = args

    def __str__(self):
        return f'{self.opcode} {self.order} {self.args}'

    # eg.  correct_format = [[SymbolType.VAR, SymbolType.String], [SymbolType.String]]
    def check_format(self, correct_format):
        ok = self._are_args_ok(correct_format)
        if not ok:
            raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE, "Wrong types for " + str(self.__str__()))

    def _are_args_ok(self, correct_format):
        if len(self.args) != len(correct_format):
            return False

        for i in range(0, len(correct_format)):
            # beware that args is dict with args starting from 1
            if self.args.get(i + 1) is None:
                return False
            if self.args.get(i + 1).type not in correct_format[i]:
                return False
        return True

    def __eq__(self, o: object) -> bool:
        return self.opcode == o.opcode and self.order == o.order and self.args == o.args
