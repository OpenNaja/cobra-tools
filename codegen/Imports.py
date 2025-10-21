import logging
from typing import TYPE_CHECKING, TextIO
if TYPE_CHECKING:
    from . import Config, Element
    from .XmlParser import XmlParser

from .naming_conventions import name_class, template_re
from .path_utils import module_path_to_import_path

NO_CLASSES = ("Padding", "self", "template")


class Imports:
    """Creates and writes an import block"""

    def __init__(self, parser: 'XmlParser', xml_struct: 'Element', gen_dir: str, for_pyi: bool = False):
        self.parent: 'XmlParser' = parser
        self.xml_struct: 'Element' = xml_struct
        self.gen_dir: str = gen_dir
        self.imports: set[str] = set()
        self.typing_imports: set[str] = set()
        # import parent class
        self.add(xml_struct.attrib.get("inherit"))

        self._collect_imports(xml_struct, for_pyi)

    def _collect_imports(self, xml_struct: 'Element', for_pyi: bool) -> None:
        """Unified logic for collecting imports for both .py and .pyi files."""

        # Define the helper function for pyi checks locally
        def should_import(type_name):
            class_name = name_class(type_name)
            is_basic_builtin = (
                class_name in self.parent.basics.booleans or
                class_name in self.parent.basics.integrals or
                class_name in self.parent.basics.floats or
                class_name in self.parent.basics.strings
            )
            return not is_basic_builtin

        # Logic for bitfields/bitflags
        if xml_struct.tag in self.parent.bitstruct_types:
            for field in xml_struct:
                if field.tag == "member":
                    field_type = field.attrib["type"]
                    if for_pyi:
                        if field_type not in self.parent.builtin_literals and should_import(field_type):
                            self.add(field_type)
                    else: # .py logic from original _collect_py_imports
                        self.add(field_type)

        # Logic for compounds/structs
        elif xml_struct.tag in self.parent.struct_types:
            for field in xml_struct:
                if field.tag in ("add", "field", "member"):
                    # Handle field type import
                    field_type = field.attrib["type"]
                    if for_pyi:
                        if should_import(field_type):
                            self.add(field_type)
                    else:
                        if not self.is_template(field_type):
                            self.add_indirect_import()

                    # Handle Array import
                    if self.parent.get_attr_with_backups(field, ["arr1", "length"]):
                        self.add("Array")

                    # Handle Template import
                    template = self.parent.get_attr_with_array_alt(field, "template")
                    if template:
                        templates = template if isinstance(template, list) else [template]
                        for t in templates:
                            template_class = name_class(t)
                            if for_pyi:
                                if not self.is_template(t) and template_class in self.parent.path_dict and should_import(template_class):
                                    self.add(template_class)
                            else:
                                if not self.is_template(template_class):
                                    self.add_indirect_import()
                    
                    # Handle Conditional (onlyT/excludeT) and Version imports
                    elements_to_check: list['Element'] = [field] + list(field.findall("default"))
                    for element in elements_to_check:
                        if for_pyi:
                            for key in ("onlyT", "excludeT"):
                                type_name: str | None = element.attrib.get(key)
                                if type_name and should_import(type_name):
                                    self.add(type_name)
                        else:
                            if element.attrib.get("onlyT") or element.attrib.get("excludeT"):
                                self.add_indirect_import()
                            if element.tag == "default" and element.attrib.get("versions"):
                                self.add("versions")

        elif xml_struct.tag == 'enum':
            pass  # No imports needed for enums

        else:
            raise NotImplementedError(f'Unknown tag type {xml_struct.tag}')

    def is_template(self, string_to_check: str) -> bool:
        return bool(template_re.fullmatch(string_to_check))

    def add(self, cls_to_import: str | None) -> None:
        if cls_to_import and cls_to_import != self.xml_struct.attrib["name"]:
            self.imports.add(cls_to_import.split('.')[0])

    def is_recursive_field(self, field: 'Element') -> bool:
        field_type = field.attrib['type']
        if field_type not in self.parent.processed_types and field_type != "template":
            if field.attrib.get('recursive', 'False') != 'True':
                logging.warning(f"Field {field.attrib['name']} with type {field_type} in format " \
                             f"{self.parent.format_name} is not a reference to a preceding type, but is not " \
                             f"marked as recursive")
            return True
        else:
            return field.attrib.get('recursive', 'False') == 'True'

    def add_indirect_import(self) -> None:
        self.add("name_type_map")

    def write(self, stream: TextIO) -> None:
        module_imports: list[str] = []
        local_imports: list[str] = []

        if self.typing_imports:
            sorted_typing = ", ".join(sorted(list(self.typing_imports)))
            module_imports.append(f"from typing import {sorted_typing}\n")

        for class_import in self.imports:
            # don't write classes that are purely virtual
            if class_import in NO_CLASSES:
                continue
            import_path = self.parent.path_dict.get(class_import, None)
            if import_path:
                local_imports.append(f"from {module_path_to_import_path(import_path, self.gen_dir)} import {class_import}\n")
            else:
                module_imports.append(f"import {class_import}\n")
        module_imports.sort()
        local_imports.sort()
        for line in module_imports + local_imports:
            stream.write(line)
        if self.imports or self.typing_imports:
            stream.write("\n\n")
