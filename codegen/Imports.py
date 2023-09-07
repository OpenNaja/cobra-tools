import os.path as path
import logging

import codegen.naming_conventions as convention


NO_CLASSES = ("Padding", "self", "template")


class Imports:
    """Creates and writes an import block"""

    def __init__(self, parser, xml_struct, gen_dir):
        self.parent = parser
        self.xml_struct = xml_struct
        self.gen_dir = gen_dir
        self.imports = set()
        # import parent class
        self.add(xml_struct.attrib.get("inherit"))

        # import classes used in the fields
        if xml_struct.tag in self.parent.bitstruct_types:
            for field in xml_struct:
                if field.tag == "member":
                    self.add(field.attrib["type"])
        elif xml_struct.tag == 'enum':
            pass
        elif xml_struct.tag in self.parent.struct_types:
            for field in xml_struct:
                if field.tag in ("add", "field", "member"):
                    field_type = field.attrib["type"]
                    if not self.is_template(field_type):
                        self.add_indirect_import()
                    arr1 = self.parent.get_attr_with_backups(field, ["arr1", "length"])
                    if arr1:
                        self.add("Array")
    
                    template = self.parent.get_attr_with_array_alt(field, "template")
                    if template:
                        if isinstance(template, list):
                            for entry in template:
                                # template can be either a type or a template
                                # only import if a type
                                template_class = convention.name_class(entry)
                                if not self.is_template(template_class):
                                    self.add_indirect_import()
                        else:
                            # template can be either a type or a template
                            # only import if a type
                            template_class = convention.name_class(template)
                            if not self.is_template(template_class):
                                self.add_indirect_import()
    
                    onlyT = field.attrib.get("onlyT")
                    excludeT = field.attrib.get("excludeT")
                    if onlyT or excludeT:
                        self.add_indirect_import()
    
                    for default in field:
                        if default.tag in ("default",):
                            if default.attrib.get("versions"):
                                self.add("versions")
                            onlyT = default.attrib.get("onlyT")
                            excludeT = default.attrib.get("excludeT")
                            if onlyT or excludeT:
                                self.add_indirect_import()
        else:
            raise NotImplementedError(f'Unknown tag type {xml_struct.tag}')

    def is_template(self, string_to_check):
        return bool(convention.template_re.fullmatch(string_to_check))

    def add(self, cls_to_import):
        if cls_to_import and cls_to_import != self.xml_struct.attrib["name"]:
            self.imports.add(cls_to_import.split('.')[0])

    def is_recursive_field(self, field):
        field_type = field.attrib['type']
        if field_type not in self.parent.processed_types and field_type != "template":
            if field.attrib.get('recursive', 'False') != 'True':
                logging.warn(f"Field {field.attrib['name']} with type {field_type} in format " \
                             f"{self.parent.format_name} is not a reference to a preceding type, but is not " \
                             f"marked as recursive")
            return True
        else:
            return field.attrib.get('recursive', 'False') == 'True'

    def add_indirect_import(self):
        self.add("name_type_map")

    def write(self, stream):
        module_imports = []
        local_imports = []
        for class_import in self.imports:
            # don't write classes that are purely virtual
            if class_import in NO_CLASSES:
                continue
            import_path = self.parent.path_dict.get(class_import, None)
            if import_path:
                local_imports.append(f"from {self.import_from_module_path(import_path, gen_dir=self.gen_dir)} import {class_import}\n")
            else:
                module_imports.append(f"import {class_import}\n")
        module_imports.sort()
        local_imports.sort()
        for line in module_imports + local_imports:
            stream.write(line)
        if self.imports:
            stream.write("\n\n")

    @staticmethod
    def import_from_module_path(module_path, gen_dir):
        return f"{gen_dir}.{module_path.replace(path.sep, '.')}"
