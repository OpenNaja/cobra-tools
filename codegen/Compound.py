from .BaseClass import BaseClass
from .Imports import Imports
from .Union import Union

FIELD_TYPES = ("add", "field")


class Compound(BaseClass):

    def read(self):
        """Create a self.struct class"""
        super().read()

        self.field_unions = []
        for field in self.struct:
            if field.tag in FIELD_TYPES:
                field_name = field.attrib["name"]
                if self.field_unions and self.field_unions[-1].name == field_name:
                    union = self.field_unions[-1]
                else:
                    union = Union(self, field_name)
                    self.field_unions.append(union)
                union.append(field)

        if not self.class_basename:
            self.class_basename = "BaseStruct"
            self.imports.add("BaseStruct")

        # write to python file
        with open(self.out_file, "w", encoding=self.parser.encoding) as f:
            # write the header stuff
            super().write(f)

            self.write_line(f)
            self.write_line(f, 1, f"_import_key = '{Imports.import_map_key(self.parser.path_dict[self.class_name])}'")
            # for now, only try to vectorize structs that explicitly allow it
            if self.struct.get("allow_np", None) == "true":
                self.write_line(f, 1, f"allow_np = True")

            # check all fields/members in this class and write them as fields
            # for union in self.field_unions.values():
            #   union.write_declaration(f)
            if "def __init__" not in self.src_code:
                self.write_line(f)
                self.write_line(f, 1, "def __init__(self, context, arg=0, template=None, set_default=True):")
                if self.struct.attrib.get("generic", "False") == "True":
                    self.write_line(f, 2, "if template is None:")
                    self.write_line(f, 3, "raise TypeError(f'{type(self).__name__} requires template is not None')")
                # the standard attributes are handled by the parent class
                self.write_line(f, 2, "super().__init__(context, arg, template, set_default=False)")

                # for ovl memory structs, some pointers may have counts that are defined before the count
                # so for init, write pointers last
                for union in self.field_unions:
                    if not union.is_ovl_ptr():
                        union.write_init(f)
                for union in self.field_unions:
                    if union.is_ovl_ptr():
                        union.write_init(f)
                self.write_line(f, 2, "if set_default:")
                self.write_line(f, 3, "self.set_defaults()")

            # write attribute list
            method_str = "_attribute_list = "
            if "_attribute_list = " not in self.src_code:
                self.write_line(f)
                self.write_line(f, 1, method_str)
                if self.class_basename:
                    f.write(f"{self.class_basename}._attribute_list + [\n\t\t")
                for union in self.field_unions:
                    union.write_attributes(f)
                f.write("]")

            # write the _get_filtered_attribute_list method
            method_str = "def _get_filtered_attribute_list(cls, instance, include_abstract=True):"
            if "def _get_filtered_attribute_list(" not in self.src_code:
                self.write_line(f)
                self.write_line(f, 1, "@classmethod")
                self.write_line(f, 1, method_str)
                condition = ""
                if self.class_basename:
                    self.write_line(f, 2, "yield from super()._get_filtered_attribute_list(instance, include_abstract)")
                for union in self.field_unions:
                    condition = union.write_filtered_attributes(f, condition, target_variable="instance")

            self.write_src_body(f)
            self.write_line(f)
