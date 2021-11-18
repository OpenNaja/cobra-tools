from os.path import sep


NO_CLASSES = ("Padding", "self")


class Imports:
    """Creates and writes an import block"""

    def __init__(self, parser, xml_struct):
        self.parent = parser
        self.xml_struct = xml_struct
        self.path_dict = parser.path_dict
        self.imports = []
        # import parent class
        self.add(xml_struct.attrib.get("inherit"))
        # import ContextReference class
        if xml_struct.tag in parser.struct_types and not xml_struct.attrib.get("inherit"):
            self.add("ContextReference")

        # import classes used in the fields
        for field in xml_struct:
            if field.tag in ("add", "field", "member"):
                field_type = field.attrib["type"]
                # template = field.attrib.get("template")
                arr1 = field.attrib.get("arr1")
                if arr1 is None:
                    arr1 = field.attrib.get("length")
                if arr1:
                    self.add(field_type, array=True)
                else:
                    self.add(field_type)

                for default in field:
                    if default.tag in ("default",):
                        if default.attrib.get("versions"):
                            self.add("versions")

    def add(self, cls_to_import, array=False):
        if cls_to_import:
            has_stream_functions, import_type = self.parent.map_type(cls_to_import, array)
            if has_stream_functions and not array and import_type in self.parent.builtin_literals:
                return
            else:
                if not array:
                    import_type = (import_type, )
            [self.imports.append(import_class.split('.')[0]) for import_class in import_type]


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
        return f"generated.{module_path.replace(sep, '.')}"
