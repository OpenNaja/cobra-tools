import logging
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Config, Element
    from .XmlParser import XmlParser

from .Basics import Basics
from .BaseClass import BaseClass
from .Imports import Imports
from .naming_conventions import name_class


class Bitfield(BaseClass):

    def __init__(self, parser: 'XmlParser', struct: 'Element', cfg: 'Config') -> None:
        super().__init__(parser, struct, cfg)

    def map_pos(self) -> None:
        """Generate position if it does not exist"""
        pos = 0
        for field in self.struct:
            num_bits = field.attrib.get("numbits")
            if num_bits:
                field.attrib["pos"] = str(pos)
                pos += int(num_bits)

    def get_mask(self) -> None:
        """Generate position if it does not exist"""
        for field in self.elements:
            if not field.attrib.get('mask'):
                if "numbits" in field.attrib:
                    num_bits = int(field.attrib["numbits"])
                elif "width" in field.attrib:
                    num_bits = int(field.attrib["width"])
                elif "bit" in field.attrib:
                    num_bits = 1
                    field.attrib["pos"] = field.attrib["bit"]
                    field.attrib["type"] = "bool"
                else:
                    raise AttributeError(
                        f"Neither width, mask, bit or numbits are defined for {field.attrib['name']}"
                    )
                pos = int(field.attrib["pos"])

                mask = ~((~0) << (pos + num_bits)) & ((~0) << pos)
                field.attrib['mask'] = str(hex(mask))

    def read(self) -> None:
        """Create a self.struct class"""
        super().read()
        storage = self.struct.attrib["storage"]
        self.imports.add(storage)
        self.imports.add("BasicBitfield")
        self.imports.add("BitfieldMember")
        self.class_basename = "BasicBitfield"

        # write to python file
        with open(self.out_file, "w", encoding=self.parser.encoding) as f:
            # write the header stuff
            super().write(f)
            self.write_line(f, 1, f"_storage = {storage}")
            self.map_pos()
            self.get_mask()
            if self.struct.tag == 'bitflags':
                for field in self.struct:
                    self.write_line(
                        f, 1, f"{field.attrib['enum_name']} = 2 ** {field.attrib['bit']}"
                    )
            for field in self.elements:
                field_name = field.attrib["name"]
                field_type = field.attrib.get("type", "int")
                if field_type not in self.parser.builtin_literals:
                    field_type = f'{field_type}.from_value'
                self.write_line(
                    f, 1, f"{field_name} = BitfieldMember(pos={field.attrib['pos']}, mask={field.attrib['mask']}, return_type={field_type})"
                )

            self.write_line(f, 0)
            self.write_line(f, 1, f"def set_defaults(self):")
            defaults = []
            for field in self.elements:
                field_name = field.attrib["name"]
                field_type = field.attrib.get("type", "int")
                field_default = field.attrib.get("default")
                # write the field's default, if it exists
                if field_default:
                    # if the default is an enum default value, access member of that enum
                    if self.parser.tag_dict[field_type.lower()] == "enum":
                        field_default = f"{field_type}.{field_default}"
                    # If we're not an enum, we need to check if we're a boolean and capitalize
                    elif self.parser.tag_dict[field_type.lower()] == "basic" and \
                        field_type in self.parser.basics.booleans:
                        if field_default.capitalize() in ("True", "False"):
                            field_default = field_default.capitalize()

                    defaults.append((field_name, field_default))
            if defaults:
                for field_name, field_default in defaults:
                    self.write_line(f, 2, f"self.{field_name} = {field_default}")
            else:
                self.write_line(f, 2, f"pass")

            self.write_src_body(f)
            self.write_line(f)

        if self.write_stubs:
            self.write_pyi()

    def write_pyi(self) -> None:
        """Writes the .pyi type stub file for this bitfield."""
        with open(self.out_pyi_file, "w", encoding=self.parser.encoding) as f:
            pyi_imports = Imports(self.parser, self.struct, self.gen_dir, for_pyi=True)
            pyi_imports.add(self.class_basename)
            pyi_imports.write(f)

            class_call = self.get_class_call().strip()
            f.write(f"{class_call[:-1] if class_call.endswith(':') else class_call}:\n")

            basics: Basics | None = self.parser.basics
            for field in self.elements:
                field_name = field.attrib["name"]
                # After conventions, type is capitalized, e.g., "Uint", "Byte"
                field_type_cased = field.attrib.get("type", "Int")
                # Map basic types to built-ins
                if basics and field_type_cased in basics.booleans:
                    type_hint = "bool"
                elif basics and field_type_cased in basics.strings:
                    type_hint = "str"
                elif basics and field_type_cased in basics.integrals:
                    type_hint = "int"
                elif basics and field_type_cased in basics.floats:
                    type_hint = "float"
                else:
                    # It's a complex type (e.g., an enum)
                    type_hint = field_type_cased

                f.write(f"    {field_name}: {type_hint}\n")

            if self.struct.tag == 'bitflags':
                for field in self.elements:
                    f.write(f"    {field.attrib['enum_name']}: int\n")
