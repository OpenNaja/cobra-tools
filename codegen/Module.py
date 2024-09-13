import os
from root_path import root_dir
from .path_utils import module_path_to_output_file_path


class Module:

    def __init__(self, parser, element, gen_dir):
        self.parser = parser
        self.element = element
        self.gen_dir = gen_dir
        self.read(element)
        self.write(parser.path_dict[element.attrib["name"]])

    def read(self, element):
        self.comment_str = element.text
        self.priority = int(element.attrib.get("priority", "0"))
        self.depends = [module for module in element.attrib.get("depends", "").split()]
        self.custom = element.attrib.get("custom", "False")

    def write(self, module_path):
        init_path = module_path_to_output_file_path(os.path.join(module_path, "__init__"), self.gen_dir, root_dir)
        with open(init_path, "w", encoding=self.parser.encoding) as file:
            file.write(self.comment_str)
            file.write(f'\n\n__priority__ = {repr(self.priority)}')
            file.write(f'\n__depends__ = {repr(self.depends)}')
            file.write(f'\n__custom__ = {self.custom}')
            file.write(f'\n')
