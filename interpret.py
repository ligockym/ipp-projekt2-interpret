import sys
from typing import TextIO, Dict, List

from ArithmeticManager import ArithmeticManager
from DataStackManager import DataStackManager
from DebugManager import DebugManager
from FrameFuncManager import *
from IOManager import IOManager
from Instruction import Instruction
from JumpManager import JumpManager
from Memory import Memory
from StringManager import StringManager
from TypeManager import TypeManager
from XmlInstructionsFactory import XmlInstructionsFactory
from InterpretError import *
import argparse


class Interpret:
    """
    Interpret is responsible for holding data about instructions, labels and counter.
    It manages whole flow of interpretation.
    """

    def __init__(self, source: TextIO, input: TextIO):
        self.input = input
        self.source = source
        self.memory = Memory()
        self.instructions: Dict[int, Instruction] = {}
        self.labels: Dict[str, int] = {}
        self.call_stack: List[int] = []
        self.counter: int = 1

        frameFuncManager = FrameFuncManager(self)
        dataStackManager = DataStackManager(self)
        arithmeticManager = ArithmeticManager(self)
        ioManager = IOManager(self)
        stringManager = StringManager(self)
        typeManager = TypeManager(self)
        jumpManager = JumpManager(self)
        debugManager = DebugManager(self)

        self.method_for_opcode = {
            "MOVE": frameFuncManager.move,
            "CREATEFRAME": frameFuncManager.create_frame,
            "PUSHFRAME": frameFuncManager.push_frame,
            "POPFRAME": frameFuncManager.pop_frame,
            "DEFVAR": frameFuncManager.defvar,
            "CALL": frameFuncManager.call,
            "RETURN": frameFuncManager.return_fn,
            "PUSHS": dataStackManager.pushs,
            "POPS": dataStackManager.pops,
            "ADD": arithmeticManager.add,
            "SUB": arithmeticManager.sub,
            "MUL": arithmeticManager.mul,
            "IDIV": arithmeticManager.idiv,
            "LT": arithmeticManager.lt,
            "GT": arithmeticManager.gt,
            "EQ": arithmeticManager.eq,
            "AND": arithmeticManager.and_fn,
            "OR": arithmeticManager.or_fn,
            "NOT": arithmeticManager.not_fn,
            "INT2CHAR": arithmeticManager.int2char,
            "STRI2INT": arithmeticManager.stri2int,
            "READ": ioManager.read,
            "WRITE": ioManager.write,
            "CONCAT": stringManager.concat,
            "STRLEN": stringManager.strlen,
            "GETCHAR": stringManager.getchar,
            "SETCHAR": stringManager.setchar,
            "TYPE": typeManager.type,
            "LABEL": jumpManager.label,
            "JUMP": jumpManager.jump,
            "JUMPIFEQ": jumpManager.jumpifeq,
            "JUMPIFNEQ": jumpManager.jumpifneq,
            "EXIT": jumpManager.exit,
            "DPRINT": debugManager.dprint,
            "BREAK": debugManager.break_fn
        }

    def parse_instructions(self):
        """
        Loads instructions from source file / stdin into dictionary and checks if all instructions have implementation
        :return:
        """
        factory = XmlInstructionsFactory()

        self.instructions = factory.load_instructions(self.source)

        # check if all instructions have implementation
        opcode_keys = self.method_for_opcode.keys()
        for key, instruction in self.instructions.items():
            if instruction.opcode not in opcode_keys:
                raise InterpretError(InterpretErrorEnum.UNEXPECTED_XML, f"Wrong opcode {instruction.opcode}")

    def run(self):
        """
        Interpretation starts on instruction with order set to 1 and then is incremented up to last instructions.
        Order numbers does not need to go in sequence but they are run in ascending order.
        :return:
        """
        if len(self.instructions) == 0:
            last_order_number = 0
        else:
            last_order_number = max(self.instructions.keys())
        while self.counter <= last_order_number:
            self.run_instruction(self.counter)
            self.counter += 1

    def save_labels_and_remove(self):
        """
        Saves all labels from instructions into own dictionary and removes them from instructions dictionary.
        :return:
        """
        for key in list(self.instructions.keys()):
            instruction = self.instructions[key]
            if instruction.opcode == 'LABEL':
                # call method for instruction and remove label instruction from instructions
                self.method_for_opcode.get('LABEL')(instruction)
                del self.instructions[key]

    def run_instruction(self, order) -> bool:
        """
        Finds correct method which will perform the instruction and executes it.
        :param order:
        :return:
        """
        instruction = self.instructions.get(order)
        if not instruction:
            return False
        method = self.method_for_opcode.get(instruction.opcode.upper())

        if method:
            method(instruction)
            return True
        else:
            raise InterpretError(InterpretErrorEnum.SEMANTIC_ERR,
                                 "I do not have implementation for " + instruction.opcode)

    def push_counter(self):
        self.call_stack.append(self.counter)

    def pop_counter(self):
        if len(self.call_stack) == 0:
            raise InterpretError(InterpretErrorEnum.NON_EXISTING_VALUE)
        self.counter = self.call_stack.pop()

    def save_label(self, label_name, label_counter):
        if label_name in self.labels:
            raise InterpretError(InterpretErrorEnum.SEMANTIC_ERR, f"Redefining label {label_name}")
        # save current counter
        self.labels[label_name] = label_counter

    def jump_label(self, label_name):
        self.does_label_exist(label_name)
        self.counter = self.labels.get(label_name)

    def does_label_exist(self, label_name):
        if label_name not in self.labels:
            raise InterpretError(InterpretErrorEnum.SEMANTIC_ERR, f"Not defined label {label_name}")

    def input_one_value(self):
        """
        Loads one value either from stdin or from file
        :return:
        """
        if self.input is None:
            # from input
            return input()
        else:
            value = self.input.readline()
            if value == '':
                return None
            return value.rstrip("\n")

    def __str__(self):
        return f"Interpret: \n Counter: {self.counter}\n Memory: {str(self.memory)}\n Labels: {str(self.labels)}"


def main():
    parser = argparse.ArgumentParser(description='Interprets XML representation of the language IPPCode22')
    parser.add_argument('--source', type=str, help='source file with XML representation of program')
    parser.add_argument('--input', type=str,
                        help='file containing input sequences for the program that is being interpreted')
    args = parser.parse_args()

    try:
        source_file = None
        input_file = None

        if args.source:
            source_file = open(args.source)
        if args.input:
            input_file = open(args.input)

        if source_file == input_file is None:
            raise InterpretError(InterpretErrorEnum.ARG_ERR, "At least one from source/input arguments have to be set.")

        interpret = Interpret(source_file, input_file)
        interpret.parse_instructions()
        interpret.save_labels_and_remove()
        interpret.run()

        if source_file:
            source_file.close()
        if input_file:
            input_file.close()
    except InterpretError as err:
        print(f"Error in instruction {interpret.counter}: ", err)
        sys.exit(err.error_type)


if __name__ == "__main__":
    main()
