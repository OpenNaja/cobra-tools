import os
import logging
from importlib import import_module

from .BaseClass import BaseClass
from .Enum import Enum
from .Imports import Imports


class Basics:

    def __init__(self, parser, basics_file, ):
        self.parser = parser
        self.base_module = None
        self.basic_map = {}
        self.basics_file = basics_file
        self.imports = []
        self.load_base_module()
        
    def load_base_module(self, ):
        # get basic.py file
        if os.path.isfile(self.basics_file):
            old_wd = os.getcwd()
            base_module = import_module(os.path.relpath(self.basics_file).replace(os.path.sep, ".")[:-3])
            self.base_module = base_module

    def read(self, xml_struct):
        basic_name = xml_struct.attrib["name"]
        if hasattr(self.base_module, basic_name):
            self.basic_map[basic_name] = getattr(self.base_module, basic_name)
        else:
            raise AttributeError(f"Basic type {basic_name} in {self.parser.format_name}.xml but not in associated basic.py module!")
        if self.suitable_for_enum(xml_struct):
            # this basic is suitable for enums
            enum_name = Enum.base_from_storage(basic_name)
            enum_path = BaseClass.get_out_path(os.path.join(self.parser.path_dict[enum_name], '__init__'))
            with open(enum_path, "a", encoding=self.parser.encoding) as f:
                # if nothing in file, add enum base class import
                if not f.tell():
                    f.write(f"from {Imports.import_from_module_path(self.parser.path_dict['BaseEnum'])} import BaseEnum\n")
                f.write(f"\nfrom {Imports.import_from_module_path(self.parser.path_dict[basic_name])} import {basic_name}\n")
                # class declaration
                f.write(f'\n\nclass {enum_name}(BaseEnum):')
                # read method for compatibility
                f.write(f'\n\n\tdef read(self, stream):')
                f.write(f'\n\t\tself._value_ = {self.parser.read_for_type(basic_name, None)}')
                # write method for compatibility
                f.write(f'\n\n\tdef write(self, stream):')
                f.write(f'\n\t\t{self.parser.write_for_type(basic_name, "self.value", None)}')
                # from_stream
                f.write(f'\n\n\t@classmethod')
                f.write(f'\n\tdef from_stream(cls, stream, context=None, arg=0, template=None):')
                f.write(f'\n\t\tinstance = cls.from_value({self.parser.read_for_type(basic_name, None)})')
                f.write(f'\n\t\treturn instance')
                # to_stream
                f.write(f'\n\n\t@classmethod')
                f.write(f'\n\tdef to_stream(cls, stream, instance):')
                f.write(f"\n\t\t{self.parser.write_for_type(basic_name, 'instance.value', None)}")
                f.write(f"\n\t\treturn instance")
                f.write(f'\n')

    def add_other_basics(self, other_basics, other_basic_path):
        to_import = []
        for basic, object in other_basics.basic_map.items():
            if basic not in self.basic_map:
                self.basic_map[basic] = object
                to_import.append(basic)
        if to_import:
            with open(self.basics_file, "a", encoding=self.parser.encoding) as f:
                f.write(f'\n\nfrom {Imports.import_from_module_path(other_basic_path)} import ')
                f.write(f'{", ".join(to_import)}')

    def write_basic_map(self, ):
        with open(self.basics_file, "a", encoding=self.parser.encoding) as f:
            f.write("\n\nbasic_map = {")
            for basic in self.basic_map:
                f.write(f"\n\t\t\t'{basic}': {basic},")
            f.write("\n}\n")

    @staticmethod
    def suitable_for_enum(basic_struct):
        return basic_struct.attrib.get("integral", "False") == "True" and basic_struct.attrib.get("countable", "True") == "True"
