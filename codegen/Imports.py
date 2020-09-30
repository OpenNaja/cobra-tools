
class Imports:
    """Creates and writes an import block"""

    def __init__(self, parser, xml_struct):
        self.parent = parser
        self.xml_struct = xml_struct
        self.path_dict = parser.path_dict
        self.imports = []
        # import parent class
        self.add(xml_struct.attrib.get("inherit"))

        # import classes used in the fields
        for field in xml_struct:
            if field.tag in ("add", "field", "member"):
                field_type = field.attrib["type"]
                template = field.attrib.get("template")
                self.add(template)
                if field_type == "self.template":
                    self.add("typing")
                else:
                    self.add(field_type)
                # arr1 needs typing.List
                arr1 = field.attrib.get("arr1")
                if arr1:
                    self.add("typing")

    def add(self, cls_to_import, import_from=None):
        if cls_to_import:
            must_import, import_type = self.parent.map_type(cls_to_import)
            if must_import:
                self.imports.append(import_type)

    def write(self, stream):
        for class_import in set(self.imports):
            if class_import in self.path_dict:
                import_path = "generated." + self.path_dict[class_import].replace("\\", ".")
                stream.write(f"from {import_path} import {class_import}\n")
            else:
                stream.write(f"import {class_import}\n")
        if self.imports:
            stream.write("\n\n")
