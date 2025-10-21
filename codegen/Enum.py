from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Config, Element
    from .XmlParser import XmlParser

from .BaseClass import BaseClass
from .naming_conventions import clean_comment_str
from .Imports import Imports


class Enum(BaseClass):

    def __init__(self, parser: 'XmlParser', struct: 'Element', cfg: 'Config') -> None:
        super().__init__(parser, struct, cfg)

    def read(self) -> None:
        """Create a struct class"""
        super().read()

        storage = self.struct.attrib["storage"]
        # todo - handle case where storage is given as size instead of name
        # store storage format in dict so it can be accessed during compound writing
        self.class_basename = "BaseEnum"
        self.imports.add("BaseEnum")
        self.imports.add(storage)
        # write to python file
        with open(self.out_file, "w", encoding=self.parser.encoding) as f:
            # write the header stuff
            super().write(f)
            self.write_line(f, 1, f"_storage = {storage}")
            self.write_line(f)
            for option in self.elements:
                if option.text:
                    f.write(clean_comment_str(option.text, indent="\t"))
                f.write(f"\n\t{option.attrib['name']} = {option.attrib['value']}")
            self.write_src_body(f)
            self.write_line(f)

        if self.write_stubs:
            self.write_pyi()

    def write_pyi(self) -> None:
        """Writes the .pyi type stub file for this enum."""
        with open(self.out_pyi_file, "w", encoding=self.parser.encoding) as f:
            pyi_imports = Imports(self.parser, self.struct, self.gen_dir, for_pyi=True)
            pyi_imports.add(self.class_basename)
            pyi_imports.write(f)

            class_call = self.get_class_call().strip()
            f.write(f"{class_call[:-1] if class_call.endswith(':') else class_call}:\n")
            
            for option in self.elements:
                option_name = option.attrib['name']
                f.write(f"    {option_name}: {self.class_name}\n")