import os
from importlib import import_module

from .Imports import Imports


class Basics:

    def __init__(self, parser, basics_file, ):
        self.parser = parser
        self.basic_map = {}
        self.booleans = set()
        self.basics_file = basics_file
        self.imports = []

    def read(self, xml_struct):
        basic_name = xml_struct.attrib["name"]

        self.parser.processed_types[basic_name] = None

        self.basic_map[basic_name] = None

        if xml_struct.attrib.get("boolean", "False") == "True":
            self.booleans.add(basic_name)

    def add_other_basics(self, other_basics, other_basic_path):
        to_import = []
        for basic, object in other_basics.basic_map.items():
            if basic not in self.basic_map:
                self.basic_map[basic] = object
                to_import.append(basic)
        self.booleans.update(other_basics.booleans)
        if to_import:
            with open(self.basics_file, "a", encoding=self.parser.encoding) as f:
                f.write(f'\n\nfrom {Imports.import_from_module_path(other_basic_path)} import ')
                f.write(f'{", ".join(to_import)}')

