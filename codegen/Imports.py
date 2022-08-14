import os.path as path

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
        for field in xml_struct:
            if field.tag in ("add", "field", "member"):
                field_type = field.attrib["type"]
                template = field.attrib.get("template")
                if template:
                    # template can be either a type or a reference to a local field
                    # only import if a type
                    template_class = convention.name_class(template)
                    if template_class in self.path_dict:
                        self.add_module(template_class)
                arr1 = field.attrib.get("arr1")
                if arr1 is None:
                    arr1 = field.attrib.get("length")
                if arr1:
                    self.add_mapped_type(field_type, array=True)
                    if xml_struct.tag in parser.struct_types:
                        self.add(field_type)
                        self.add("Array")
                else:
                    self.add_mapped_type(field_type)
                    if xml_struct.tag in parser.struct_types:
                        self.add(field_type)
                for default in field:
                    if default.tag in ("default",):
                        if default.attrib.get("versions"):
                            self.add("versions")

    def add_mapped_type(self, cls_to_import, array=False):
        if cls_to_import:
            has_stream_functions, import_type = self.parent.map_type(cls_to_import, array)
            if has_stream_functions and not array and import_type in self.parent.builtin_literals:
                # import not necessary (read/write on stream, and init can happen from literal)
                return
            else:
                if not array:
                    import_type = (import_type, )
            [self.add(import_class) for import_class in import_type]

    def add(self, cls_to_import):
        if cls_to_import:
            self.imports.append(cls_to_import.split('.')[0])

    def add_module(self, cls_to_import):
        # provide class access through the module to prevent circular import
        if cls_to_import:
            self.imports.append(self.import_from_module_path(self.path_dict[cls_to_import]))

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
