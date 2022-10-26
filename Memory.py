from typing import List
from Frame import Frame
from FrameType import FrameType
from InterpretError import InterpretError, InterpretErrorEnum
from Symbol import Symbol, SymbolType
from Variable import Variable


class Memory:

    def __init__(self):
        self.global_frame = Frame()
        self.temp_frame: Frame = None  #
        self.local_frames: List[Frame] = []
        self.data_stack: List[Symbol] = []

    def get_frame(self, frame_type: FrameType) -> Frame:
        """
        Returns frame by its type.
        :param frame_type:
        :return:
        """
        if frame_type == FrameType.GF:
            return self.global_frame
        elif frame_type == FrameType.LF:
            return self.get_local_frame()
        else:
            if self.temp_frame is None:
                raise InterpretError(InterpretErrorEnum.NON_EXISTING_FRAME)
            return self.temp_frame

    def get_local_frame(self):
        """
        Returns actual local frame
        :return:
        """
        if len(self.local_frames) == 0:
            raise InterpretError(InterpretErrorEnum.NON_EXISTING_FRAME)
        return self.local_frames[-1]

    def new_local_frame(self):
        self.local_frames.append(Frame())

    def new_temp_frame(self):
        self.temp_frame = Frame()

    def push_temp_to_local(self):
        if self.temp_frame is None:
            raise InterpretError(InterpretErrorEnum.NON_EXISTING_FRAME)
        self.local_frames.append(self.temp_frame)
        self.temp_frame = None

    def pop_local_to_temp(self):
        self.temp_frame = self.get_local_frame() # could use pop, but that would raise wrong exception
        self.local_frames.pop() # pop local frame

    def def_variable(self, var_name: str, frame: FrameType):
        frame = self.get_frame(frame)
        frame.define_variable(var_name)

    def get_variable(self, var_name: str, frame: FrameType) -> Variable:
        frame = self.get_frame(frame)
        if var_name not in frame.variables:
            raise InterpretError(InterpretErrorEnum.NON_EXISTING_VAR, f"Non existing variable {var_name}")
        return frame.variables.get(var_name)

    def symbol_or_var_symbol(self, symbol: Symbol, check_if_initialized: bool = True) -> Symbol:
        """
        Returns real value from symbol, or in case of variable, finds variable in memory and returns its symbol_value.
        """
        if symbol.type != SymbolType.VAR:
            return symbol

        # is variable -> check if initialized
        variable: Variable = self.get_variable(symbol.value, symbol.frame)
        if check_if_initialized and (variable.symbol_value.type == SymbolType.NOT_INITIALIZED):
            raise InterpretError(InterpretErrorEnum.NON_EXISTING_VALUE, "Not initialized value")
        return variable.symbol_value

    def push_data_stack(self, symbol: Symbol):
        self.data_stack.append(symbol)

    def pop_data_stack(self) -> Symbol:
        if len(self.data_stack) == 0:
            raise InterpretError(InterpretErrorEnum.NON_EXISTING_VALUE, "Data stack is empty, cannot pop")
        return self.data_stack.pop()

    def __str__(self):
        return f"Global: {self.global_frame}\n Local frames: {self.local_frames}\n Temporary frame: {self.temp_frame}"