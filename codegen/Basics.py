import os
from importlib import import_module

from .Imports import Imports


class Basics:

    def __init__(self, parser, basics_file, ):
        self.parser = parser
        self.base_module = None
        self.basic_map = {}
        self.booleans = set()
        self.basics_file = basics_file
        self.imports = []
        self.load_base_module()
        
    def load_base_module(self, ):
        # get basic.py file
        if os.path.isfile(self.basics_file):
            base_module = import_module(os.path.relpath(self.basics_file).replace(os.path.sep, ".")[:-3])
            self.base_module = base_module

    def read(self, xml_struct):
        basic_name = xml_struct.attrib["name"]
        if hasattr(self.base_module, basic_name):
            self.basic_map[basic_name] = getattr(self.base_module, basic_name)
            if xml_struct.attrib.get("boolean", "False") == "True":
                self.booleans.add(basic_name)
        else:
            raise AttributeError(f"Basic type {basic_name} in {self.parser.format_name}.xml but not in associated basic.py module!")

    def add_other_basics(self, other_basics, other_basic_path):
        to_import = []
        for basic, object in other_basics.basic_map.items():
            if basic not in self.basic_map:
                self.basic_map[basic] = object
                self.booleans.add(basic)
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
