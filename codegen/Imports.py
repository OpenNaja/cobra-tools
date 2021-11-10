from os.path import sep


NO_CLASSES = ("Padding",)


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
                # self.add(template)
                # if field_type == "self.template":
                #     self.add("typing")
                # else:
                #     self.add(field_type)
                self.add(field_type)
                # arr1 needs typing.List
                arr1 = field.attrib.get("arr1")
                if arr1 is None:
                    arr1 = field.attrib.get("length")
                if arr1:
                    self.add("typing")
                    self.add("Array")
                type_attribs = ("onlyT", "excludeT")
                for attrib in type_attribs:
                    attrib_type = field.attrib.get(attrib)
                    if attrib_type:
                        self.add(attrib_type)

                for default in field:
                    if default.tag in ("default",):
                        for attrib in type_attribs:
                            attrib_type = default.attrib.get(attrib)
                            if attrib_type:
                                self.add(attrib_type)

    def add(self, cls_to_import, array=False):
        if cls_to_import:
            must_import, import_type = self.parent.map_type(cls_to_import, array)
            if must_import:
                self.imports.append(import_type)

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
