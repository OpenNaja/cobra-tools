import collections
from .BaseClass import BaseClass
from .Union import Union, get_params

FIELD_TYPES = ("add", "field")
VER = "self.context.version"


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
            arg, template, arr1, arr2, conditionals, field_name, field_type, pad_mode = get_params(field)

        # write to python file
        with open(self.out_file, "w", encoding=self.parser.encoding) as f:
            # write the header stuff
            super().write(f)

            if not self.class_basename:
                self.write_line(f)
                self.write_line(f, 1, "context = ContextReference()")

            # check all fields/members in this class and write them as fields
            # for union in self.field_unions.values():
            #   union.write_declaration(f)
            if "def __init__" not in self.src_code:
                self.write_line(f)
                self.write_line(f, 1, "def __init__(self, context, arg=None, template=None, set_default=True):")
                # classes that this class inherits from have to be read first
                if self.class_basename:
                    # context is set by the parent class
                    super_line = f"super().__init__(context, arg, template)"
                else:
                    # no inheritance, so set context
                    super_line = f"self._context = context"
                self.write_lines(f, 2, (
                    "self.name = ''",
                    super_line,
                    "self.arg = arg",
                    "self.template = template",
                    "self.io_size = 0",
                    "self.io_start = 0"
                ))

                for union in self.field_unions:
                    union.write_init(f)
                self.write_line(f, 2, "if set_default:")
                self.write_line(f, 3, "self.set_defaults()")

            if "def set_defaults(" not in self.src_code:
                self.write_line(f)
                self.write_line(f, 1, "def set_defaults(self):")
                end = f.tell()
                # write all fields, merge conditions
                condition = ""
                for union in self.field_unions:
                    condition = union.write_defaults(f, condition)
                # if no defaults have been written
                if f.tell() == end:
                    self.write_line(f, 2, "pass")

            # write the load() method
            for method_type in ("read", "write"):
                method_str = f"def {method_type}(self, stream):"
                # check all fields/members in this class and write them as fields
                if method_str in self.src_code:
                    continue
                self.write_line(f)
                self.write_line(f, 1, method_str)
                self.write_line(f, 2, "self.io_start = stream.tell()")
                # classes that this class inherits from have to be read first
                if self.class_basename:
                    self.write_line(f, 2, f"super().{method_type}(stream)")

                # write all fields, merge conditions
                condition = ""
                for union in self.field_unions:
                    condition = union.write_io(f, method_type, condition)

                self.write_line(f)
                self.write_line(f, 2, "self.io_size = stream.tell() - self.io_start")

            if "def __repr__(" not in self.src_code:
                self.write_line(f)
                self.write_line(f, 1, "def get_info_str(self):")
                self.write_line(f, 2, f"return f'{self.class_name} [Size: {{self.io_size}}, Address: {{self.io_start}}] {{self.name}}'")

                self.write_line(f)
                self.write_line(f, 1, "def get_fields_str(self):")
                self.write_line(f, 2, "s = ''")
                if self.class_basename:
                    self.write_line(f, 2, "s += super().get_fields_str()")
                for union in self.field_unions:
                    rep = f"self.{union.name}.__repr__()"
                    self.write_line(f, 2, f"s += f'\\n\t* {union.name} = {{{rep}}}'")
                self.write_line(f, 2, "return s")

                self.write_line(f)
                self.write_line(f, 1, "def __repr__(self):")
                self.write_lines(f, 2, (
                    "s = self.get_info_str()",
                    "s += self.get_fields_str()",
                    "s += '\\n'",
                    "return s"
                ))

            f.write(self.grab_src_snippet("# START_CLASS"))
            self.write_line(f)
