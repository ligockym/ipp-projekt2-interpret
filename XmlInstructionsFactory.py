import sys
from typing import List, Dict
from xml.etree.ElementTree import Element
from InterpretError import *
from Symbol import Symbol, SymbolType
from Instruction import Instruction
import xml.etree.ElementTree as ET


class XmlInstructionsFactory:

    def load_instructions(self, source) -> Dict[int, Instruction]:
        """
        Loads instructions from XML file into dictionary. If source is None, then use stdin.
        :param source:
        :return:
        """
        instructions: Dict[int, Instruction] = {}

        if source is None:
            source = sys.stdin

        try:
            xml_source = ET.parse(source)
        except Exception as exc:
            raise InterpretError(InterpretErrorEnum.WRONG_XML_FORMAT, str(exc))
        program_xml = xml_source.getroot()
        if program_xml.tag != 'program' or program_xml.attrib['language'] != 'IPPcode22':
            raise InterpretError(InterpretErrorEnum.UNEXPECTED_XML, "Wrong program tag")

        # load all instructions to program
        for child_xml in program_xml:
            if child_xml.tag != 'instruction':
                raise InterpretError(InterpretErrorEnum.UNEXPECTED_XML)

            instruction: Instruction = self._create_instruction(child_xml)

            # check whether order is not already defined
            if instruction.order in instructions:
                raise InterpretError(InterpretErrorEnum.UNEXPECTED_XML)
            # save instruction with its id
            instructions[int(instruction.order)] = instruction
        return instructions

    def _create_instruction(self, xml_node: Element) -> Instruction:
        opcode = xml_node.attrib.get('opcode')
        order = xml_node.attrib.get('order')
        args = self._build_args(xml_node)

        try:
            order = int(order)
        except (ValueError, TypeError):
            raise InterpretError(InterpretErrorEnum.UNEXPECTED_XML)

        if not isinstance(opcode, str) or order <= 0:
            raise InterpretError(InterpretErrorEnum.UNEXPECTED_XML)

        return Instruction(opcode, int(order), args)

    def _build_args(self, xml_node: Element) -> Dict[int, Symbol]:
        """
        Validates and builds arguments from xml node into dictionary, where key is arg number
        :param xml_node:
        :return:
        """
        args: Dict[int, Symbol] = {}
        for child_node in xml_node:
            if child_node.tag not in ['arg1', 'arg2', 'arg3']:
                raise InterpretError(InterpretErrorEnum.UNEXPECTED_XML)
            value = child_node.text
            arg_number = int(child_node.tag[3:])  # arg2 -> 2

            try:
                # generate from enum
                symbol_type = SymbolType[child_node.attrib['type'].upper()]
            except KeyError:
                raise InterpretError(InterpretErrorEnum.UNEXPECTED_XML, "Cannot find SymbolType")
            if arg_number in args:
                raise InterpretError(InterpretErrorEnum.UNEXPECTED_XML)
            args[arg_number] = Symbol(symbol_type, value)

        for i in range(1, len(args) + 1):
            if args.get(i) is None:
                raise InterpretError(InterpretErrorEnum.UNEXPECTED_XML, f"Wrong arguments")

        return args
