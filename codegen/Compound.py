import collections
import re

from .BaseClass import BaseClass
from .Union import Union

FIELD_TYPES = ("add", "field")
from_stream_re = re.compile(r"def from_stream\((([a-z]*), )?stream, context(=.*)?, arg(=.*)?, template.*\):")
to_stream_re = re.compile(r"def to_stream\((([a-z]*), )?stream, instance\):")


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

            # check all fields/members in this class and write them as fields
            # for union in self.field_unions.values():
            #   union.write_declaration(f)
            if "def __init__" not in self.src_code:
                self.write_line(f)
                self.write_line(f, 1, "def __init__(self, context, arg=0, template=None, set_default=True):")
                if self.struct.attrib.get("generic", "False") == "True":
                    self.write_line(f, 2, "if template is None:")
                    self.write_line(f, 3, "raise TypeError(f'{type(self).__name__} requires template is not None')")
                # classes that this class inherits from have to be read first
                if self.class_basename:
                    # the standard attributes are handled by the parent class
                    # todo - needs testing
                    self.write_line(f, 2, "super().__init__(context, arg, template, set_default=False)")
                    # self.write_line(f, 2, "super().__init__(context, arg, template, set_default)")
                else:
                    # no inheritance, so set the standard attributes
                    self.write_lines(f, 2, (
                        "self.name = ''",
                        "self._context = context",
                        "self.arg = arg",
                        "self.template = template",
                        "self.io_size = 0",
                        "self.io_start = 0"
                    ))

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

            if "def set_defaults(" not in self.src_code:
                self.write_line(f)
                self.write_line(f, 1, "def set_defaults(self):")
                # todo - needs testing
                if self.class_basename:
                    self.write_line(f, 2, f"super().set_defaults()")
                # self.write_line(f, 2, "print(f'set_defaults {self.__class__.__name__}')")
                end = f.tell()
                # write all fields, merge conditions
                condition = ""
                # for ovl memory structs, some pointers may have counts that are defined before the count
                # so for set_defaults, write pointers last
                for union in self.field_unions:
                    if not union.is_ovl_ptr():
                        condition = union.write_defaults(f, condition)
                for union in self.field_unions:
                    if union.is_ovl_ptr():
                        condition = union.write_defaults(f, condition)
                # if no defaults have been written
                if f.tell() == end:
                    self.write_line(f, 2, "pass")

            # write the read_fields/write_fields methods
            for method_type in ("read", "write"):
                method_str = f"def {method_type}_fields(cls, stream, instance):"
                if method_str in self.src_code:
                    continue
                self.write_line(f)
                self.write_line(f, 1, '@classmethod')
                self.write_line(f, 1, method_str)
                # classes that this class inherits from have to be read/written first

                if self.class_basename:
                    self.write_line(f, 2, f"super().{method_type}_fields(stream, instance)")

                # write all fields, merge conditions
                condition = ""
                for union in self.field_unions:
                    condition = union.write_io(f, method_type, condition, target_variable="instance")
                # for ovl memory structs, some pointers may have counts that are defined before the count
                # so for set_defaults, write pointers last
                for union in self.field_unions:
                    if union.is_ovl_ptr():
                        condition = union.write_arg_update(f, method_type)
                # handle empty structs
                if not self.field_unions:
                    self.write_line(f, 2, "pass")

            # write the _get_filtered_attribute_list method
            method_str = "def _get_filtered_attribute_list(cls, instance):"
            if "def _get_filtered_attribute_list(" not in self.src_code:
                self.write_line(f)
                self.write_line(f, 1, "@classmethod")
                self.write_line(f, 1, method_str)
                condition = ""
                if self.class_basename:
                    self.write_line(f, 2, "yield from super()._get_filtered_attribute_list(instance)")
                for union in self.field_unions:
                    condition = union.write_filtered_attributes(f, condition, target_variable="instance")

            if "def __repr__(" not in self.src_code:
                self.write_line(f)
                self.write_line(f, 1, "def get_info_str(self, indent=0):")
                self.write_line(f, 2, f"return f'{self.class_name} [Size: {{self.io_size}}, Address: {{self.io_start}}] {{self.name}}'")

                self.write_line(f)
                self.write_line(f, 1, "def get_fields_str(self, indent=0):")
                self.write_line(f, 2, "s = ''")
                if self.class_basename:
                    self.write_line(f, 2, "s += super().get_fields_str()")
                for union in self.field_unions:
                    # rep = f"self.{union.name}.__repr__(indent+1)"
                    rep = f"self.fmt_member(self.{union.name}, indent+1)"
                    self.write_line(f, 2, f"s += f'\\n\t* {union.name} = {{{rep}}}'")
                self.write_line(f, 2, "return s")

                self.write_line(f)
                self.write_line(f, 1, "def __repr__(self, indent=0):")
                self.write_lines(f, 2, (
                    "s = self.get_info_str(indent)",
                    "s += self.get_fields_str(indent)",
                    "s += '\\n'",
                    "return s"
                ))

            f.write(self.grab_src_snippet("# START_CLASS"))
            self.write_line(f)
