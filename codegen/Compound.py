import os
from itertools import groupby
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Config, Element
    from .XmlParser import XmlParser

from .BaseClass import BaseClass
from .Union import Union
from .Imports import Imports
from .naming_conventions import template_re

FIELD_TYPES = ("add", "field")


class Compound(BaseClass):

    def __init__(self, parser: 'XmlParser', struct: 'Element', cfg: 'Config') -> None:
        super().__init__(parser, struct, cfg)

    def read(self) -> None:
        """Create a self.struct class"""
        super().read()

        self.field_unions = []
        relevant_fields = (field for field in self.struct if field.tag in FIELD_TYPES)
        for field_name, members in groupby(relevant_fields, key=lambda f: f.attrib["name"]):
            union = Union(self, field_name)
            union.members.extend(list(members)) # Add all members from the group at once
            self.field_unions.append(union)

        if not self.class_basename:
            self.class_basename = "BaseStruct"
            self.imports.add("BaseStruct")

        # write to python file
        with open(self.out_file, "w", encoding=self.parser.encoding) as f:
            # write the header stuff
            super().write(f)

            self.write_line(f)
            if self.struct.get("allow_np", False):
                self.write_line(f, 1, f"allow_np = True")

            # handle more-than-one length attributes as properties, to keep it synced with the main one
            nr_args = int(self.struct.attrib.get("args", "1"))
            if nr_args > 1:
                self.write_line(f)
                for i in range(nr_args):
                    self.write_line(f, 1, "@property")
                    self.write_line(f, 1, f"def arg_{i + 1}(self):")
                    self.write_line(f, 2, f"return self.arg[{i}]")

            nr_templates = int(self.struct.attrib.get("templates", "1"))
            if nr_templates > 1:
                self.write_line(f)
                for i in range(nr_templates):
                    self.write_line(f, 1, "@property")
                    self.write_line(f, 1, f"def template_{i + 1}(self):")
                    self.write_line(f, 2, f"return self.template[{i}]")

            # check all fields/members in this class and write them as fields
            # for union in self.field_unions.values():
            #   union.write_declaration(f)
            if "def __init__" not in self.src_code:
                self.write_line(f)
                self.write_line(f, 1, "def __init__(self, context, arg=0, template=None, set_default=True):")

                # compound with generic="true" must have a template provided
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
            method_str = "def _get_attribute_list(cls):"
            if method_str not in self.src_code:
                self.write_line(f)
                self.write_line(f, 1, "@classmethod")
                self.write_line(f, 1, method_str)
                if self.class_basename:
                    self.write_line(f, 2, "yield from super()._get_attribute_list()")
                for union in self.field_unions:
                    union.write_attributes(f)

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

        if self.write_stubs:
            self.write_pyi()

    def write_pyi(self) -> None:
        """Writes the .pyi type stub file for this class."""
        if os.path.exists(self.out_pyi_file):
            return  # Do not overwrite the hand-written stub file.

        # Initialization
        pyi_imports = Imports(self.parser, self.struct, self.gen_dir, for_pyi=True)
        pyi_imports.add(self.class_basename)

        is_generic = self.class_name in self.parser.generic_types
        needs_union = False
        has_numpy_array_field = False
        attribute_lines = []

        for union in self.field_unions:
            # Determine the type hint for the current attribute
            type_hint = ""
            if self.class_name == "Pointer" and union.name == "data":
                type_hint = "_T"
                is_generic = True
            else:
                member = union.members[0]
                member_template = self.parser.get_attr_with_array_alt(member, "template")
                is_templated_with_tvar = member_template and isinstance(member_template, str) and template_re.fullmatch(member_template)
                
                if is_generic and is_templated_with_tvar:
                    base_type = union.get_type_hint(member)
                    type_hint = base_type.replace("[object]", "[_T]")
                else:
                    union_types = sorted(list({union.get_type_hint(m) for m in union.members}))
                    if len(union_types) > 1:
                        type_hint = f"Union[{', '.join(union_types)}]"
                        needs_union = True # Flag that a Union is required
                    else:
                        type_hint = union_types[0] if union_types else "object"
            
            attribute_lines.append(f"    {union.name}: {type_hint}\n")

            # Check for numpy array fields
            if not has_numpy_array_field:
                for member in union.members:
                    if (member.attrib["type"] in self.parser.numpy_types and 
                            self.parser.get_attr_with_backups(member, ["arr1", "length"])):
                        has_numpy_array_field = True
                        break

        # File Writing
        with open(self.out_pyi_file, "w", encoding=self.parser.encoding) as f:
            # Propagate generic status from parent class
            if not is_generic and self.class_basename:
                is_generic = self.class_basename in self.parser.generic_types

            # Add imports based on flags set during the loop
            if is_generic:
                pyi_imports.typing_imports.add("TypeVar")
                if self.class_basename not in self.parser.generic_types:
                    pyi_imports.typing_imports.add("Generic")
            if needs_union:
                pyi_imports.typing_imports.add("Union")
            if has_numpy_array_field:
                pyi_imports.add("numpy as np")

            # Special import for ArrayPointer/ForEachPointer
            if self.class_name in ("ArrayPointer", "ForEachPointer"):
                pyi_imports.add("Array")

            pyi_imports.write(f)

            if is_generic:
                f.write("_T = TypeVar(\"_T\")\n\n")

            # Construct the class definition line
            class_call = self.get_class_call().strip()
            class_def = class_call[:-1] if class_call.endswith(':') else class_call
            if is_generic:
                parent_is_generic = self.class_basename in self.parser.generic_types
                if parent_is_generic:
                    if self.class_name in ("ArrayPointer", "ForEachPointer"):
                        class_def = class_def.replace(f"({self.class_basename})", f"({self.class_basename}[Array[_T]])")
                    else:
                        class_def = class_def.replace(f"({self.class_basename})", f"({self.class_basename}[_T])")
                else:
                    if "(" in class_def and ")" in class_def:
                        closing_paren_index = class_def.rfind(')')
                        class_def = f"{class_def[:closing_paren_index]}, Generic[_T]){class_def[closing_paren_index+1:]}"
                    else:
                        class_def += f"(Generic[_T])"
            
            f.write(f"{class_def}:\n")

            # Write the attributes collected during the loop
            if not attribute_lines:
                f.write("    pass\n")
            else:
                f.writelines(attribute_lines)

            f.write("\n    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...\n")
