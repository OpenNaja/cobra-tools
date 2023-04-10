import os.path as path
import logging

import codegen.naming_conventions as convention


NO_CLASSES = ("Padding", "self", "template")


class Imports:
    """Creates and writes an import block"""

    def __init__(self, parser, xml_struct):
        self.parent = parser
        self.xml_struct = xml_struct
        self.path_dict = parser.path_dict
        self.imports = []
        # import parent class
        self.add(xml_struct.attrib.get("inherit"))
        # self.add("basic")

        # import classes used in the fields
        if xml_struct.tag in self.parent.bitstruct_types:
            for field in xml_struct:
                if field.tag == "member":
                    self.add_mapped_type(field.attrib["type"])
        elif xml_struct.tag == 'enum':
            pass
        elif xml_struct.tag in self.parent.struct_types:
            for field in xml_struct:
                if field.tag in ("add", "field", "member"):
                    field_type = field.attrib["type"]
                    is_recursive = self.is_recursive_field(field)
                    arr1 = field.attrib.get("arr1")
                    if arr1 is None:
                        arr1 = field.attrib.get("length")
                    if arr1:
                        self.add_mapped_type(field_type, array=True, exclude_cls=is_recursive)
                        if xml_struct.tag in parser.struct_types:
                            if not is_recursive:
                                self.add(field_type)
                            self.add("Array")
                    else:
                        self.add_mapped_type(field_type, exclude_cls=is_recursive)
                        if xml_struct.tag in parser.struct_types and not is_recursive:
                            self.add(field_type)
    
                    template = field.attrib.get("template")
                    if template:
                        # template can be either a type or a reference to a local field
                        # only import if a type
                        template_class = convention.name_class(template)
                        if template_class in self.path_dict:
                            self.add_indirect_import(template_class)
    
                    onlyT = field.attrib.get("onlyT")
                    if onlyT:
                        self.add_indirect_import(onlyT)
    
                    excludeT = field.attrib.get("excludeT")
                    if excludeT:
                        self.add_indirect_import(excludeT)
    
                    for default in field:
                        if default.tag in ("default",):
                            if default.attrib.get("versions"):
                                self.add("versions")
                            onlyT = default.attrib.get("onlyT")
                            if onlyT:
                                self.add_indirect_import(onlyT)
                            excludeT = default.attrib.get("excludeT")
                            if excludeT:
                                self.add_indirect_import(excludeT)

    def add_mapped_type(self, cls_to_import, array=False, exclude_cls=False):
        if cls_to_import:
            import_type = self.parent.map_type(cls_to_import, array)
            if not array:
                if import_type in self.parent.builtin_literals:
                    # import not necessary (read/write on stream, and init can happen from literal)
                    return
                else:
                    import_type = (import_type, )
            if exclude_cls:
                import_type = (cls for cls in import_type if cls != cls_to_import)
            [self.add(import_class) for import_class in import_type]

    def add(self, cls_to_import):
        if cls_to_import and cls_to_import != self.xml_struct.attrib["name"]:
            self.imports.append(cls_to_import.split('.')[0])

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

    def add_indirect_import(self, cls_to_import):
        # import the class directly, but only if it's not a struct (because those could lead to circular imports)
        if cls_to_import and self.parent.tag_dict[cls_to_import.lower()] not in self.parent.struct_types:
            self.add(cls_to_import)

    def write(self, stream):
        module_imports = []
        local_imports = []
        for class_import in set(self.imports):
            # don't write classes that are purely virtual
            if class_import in NO_CLASSES:
                continue
            if class_import in self.path_dict:
                import_path = self.import_from_module_path(self.path_dict[class_import])
                local_imports.append(f"from {import_path} import {class_import}\n")
            else:
                module_imports.append(f"import {class_import}\n")
        module_imports.sort()
        local_imports.sort()
        for line in module_imports + local_imports:
            stream.write(line)
        if self.imports:
            stream.write("\n\n")

    @staticmethod
    def import_from_module_path(module_path):
        return f"generated.{module_path.replace(path.sep, '.')}"

    @staticmethod
    def import_map_key(module_path):
        return Imports.import_from_module_path(module_path).replace("generated.formats.", "")

    @classmethod
    def write_import_map(cls, parser, file):
        with open(file, "w", encoding=parser.encoding) as f:
            f.write("from importlib import import_module\n")
            f.write("\n\ntype_module_name_map = {\n")
            for type_name in parser.processed_types:
                f.write(f"\t'{type_name}': '{cls.import_from_module_path(parser.path_dict[type_name])}',\n")
            f.write('}\n')
            f.write("\nname_type_map = {}\n")
            f.write("for type_name, module in type_module_name_map.items():\n")
            f.write("\tname_type_map[type_name] = getattr(import_module(module), type_name)\n")
            f.write("for class_object in name_type_map.values():\n")
            f.write("\tif callable(getattr(class_object, 'init_attributes', None)):\n")
            f.write("\t\tclass_object.init_attributes()")
