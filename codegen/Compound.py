import collections
import re

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

            # if "def set_defaults(" not in self.src_code:
            #     self.write_line(f)
            #     self.write_line(f, 1, "def set_defaults(self):")
            #     # todo - needs testing
            #     if self.class_basename:
            #         self.write_line(f, 2, f"super().set_defaults()")
            #     # self.write_line(f, 2, "print(f'set_defaults {self.__class__.__name__}')")
            #     end = f.tell()
            #     # write all fields, merge conditions
            #     condition = ""
            #     # for ovl memory structs, some pointers may have counts that are defined before the count
            #     # so for set_defaults, write pointers last
            #     for union in self.field_unions:
            #         if not union.is_ovl_ptr():
            #             condition = union.write_defaults(f, condition)
            #     for union in self.field_unions:
            #         if union.is_ovl_ptr():
            #             condition = union.write_defaults(f, condition)
            #     # if no defaults have been written
            #     if f.tell() == end:
            #         self.write_line(f, 2, "pass")

            # write the read_fields/write_fields methods
            # for method_type in ("read", "write"):
            #     method_str = f"def {method_type}_fields(cls, stream, instance):"
            #     if method_str in self.src_code:
            #         continue
            #     self.write_line(f)
            #     self.write_line(f, 1, '@classmethod')
            #     self.write_line(f, 1, method_str)
            #     # classes that this class inherits from have to be read/written first

            #     if self.class_basename:
            #         self.write_line(f, 2, f"super().{method_type}_fields(stream, instance)")

            #     # write all fields, merge conditions
            #     condition = ""
            #     for union in self.field_unions:
            #         condition = union.write_io(f, method_type, condition, target_variable="instance")
            #     # for ovl memory structs, some pointers may have counts that are defined before the count
            #     # so for set_defaults, write pointers last
            #     for union in self.field_unions:
            #         if union.is_ovl_ptr():
            #             condition = union.write_arg_update(f, method_type)
            #     # handle empty structs
            #     if not self.field_unions:
            #         self.write_line(f, 2, "pass")

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

            f.write(self.grab_src_snippet("# START_CLASS"))
            self.write_line(f)
