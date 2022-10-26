from enum import Enum

from FrameType import FrameType
from InterpretError import InterpretErrorEnum, InterpretError
import re

class SymbolType(Enum):
    INT='int'
    BOOL='bool'
    STRING='string'
    NIL='nil'
    LABEL='label'
    TYPE='type'
    VAR='var',
    NOT_INITIALIZED= 'not_initialized'

class SymbolTypeHelper:
    DATABLE=[SymbolType.INT, SymbolType.BOOL, SymbolType.STRING, SymbolType.VAR]
    DATABLE_NIL=[SymbolType.INT, SymbolType.BOOL, SymbolType.STRING, SymbolType.NIL, SymbolType.VAR]

class Symbol:
    def __init__(self, type: SymbolType, value):
        self.type: SymbolType = type
        self.value = value

        try:
            # eg. LF@var1
            if self.type == SymbolType.VAR:
                self.frame = FrameType[value[0:2]] # LF
                self.value = value[3:] # var1
            elif self.type == SymbolType.INT:
                self.value = int(self.value)
            elif self.type == SymbolType.NIL:
                self.value = 'nil'
            elif self.type == SymbolType.BOOL:
                if self.value.lower() == 'true':
                    self.value = True
                else:
                    self.value = False # including all other values
            elif self.type == SymbolType.TYPE:
                # in case of type, the value is the type
                self.value = SymbolType[self.value.upper()]
            elif self.type == SymbolType.STRING:
                if self.value is None:
                    self.value = ""
                self.value = self._parse_string(self.value)
        except (ValueError, TypeError):
            raise InterpretError(InterpretErrorEnum.UNEXPECTED_XML, "Wrong value")

    def __eq__(self, o: object) -> bool:
        return self.type == o.type and self.value == o.value

    # used for dprint
    def __str__(self):
        return f"Symbol {self.type}: {self.value}"

    # used for value
    def to_str(self):
        if self.type == SymbolType.NIL:
            return ''
        elif self.type == SymbolType.BOOL:
            return 'true' if self.value else 'false'
        else:
            return str(self.value)

    def type_to_str(self):
        if self.type == SymbolType.NIL:
            return 'nil'
        elif self.type == SymbolType.BOOL:
            return 'bool'
        elif self.type == SymbolType.STRING:
            return 'string'
        elif self.type == SymbolType.INT:
            return 'int'
        elif self.type == SymbolType.NOT_INITIALIZED:
            return ''

    # find \ddd occurence
    def _parse_string(self, value: str) -> str:
        pattern = re.compile(r"\\(\d{3})")
        for match in pattern.finditer(value):
            numeric_value_of_char = int(match.group(1))
            if not(0 <= numeric_value_of_char <= 999):
                raise InterpretError(InterpretErrorEnum.WRONG_OPERAND_TYPE)
            value = value.replace(match.group(0), chr(numeric_value_of_char))
        return value
