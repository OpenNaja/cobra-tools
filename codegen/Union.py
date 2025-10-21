import logging
from itertools import chain
from dataclasses import dataclass
from re import Match
from typing import TYPE_CHECKING, TextIO, TypeAlias, NewType
if TYPE_CHECKING:
    from . import Config, Element
    from .Basics import Basics
    from .Compound import Compound
    from .XmlParser import XmlParser

from .expression import Expression, Version, interpret_literal
from .Versions import Versions
from .naming_conventions import name_class, name_enum_key_if_necessary, clean_comment_str, template_re


CONTEXT_SUFFIX = "context"

XmlType: TypeAlias = str | tuple[str | None, ...] | None
XmlStr: TypeAlias = str | None
XmlVersion: TypeAlias = Version | None
XmlExpr: TypeAlias = Expression | None
ArrayExprTuple = NewType('ArrayExprTuple', tuple[XmlExpr, XmlExpr, XmlExpr])


@dataclass
class FieldParams:
    """A structured container for parameters returned by get_params."""
    arg: str
    template: XmlType
    arrays: ArrayExprTuple
    conditionals: tuple[list[str], list[str]]
    name: str
    field_type: str
    field_type_access: str
    optional: str
    default: XmlStr


def condition_indent(base_indent: str, conditionals: tuple[list[str], list[str]], condition: str = "") -> tuple[str, str]:
    # determine the python condition and indentation level based on whether the
    # last used condition was the same.
    flat_conditionals = tuple(chain.from_iterable(conditionals))
    if flat_conditionals:
        new_condition = f"if {' and '.join(flat_conditionals)}:"
        # condition is there but has not changed, so we can keep it in the same if clause
        if condition == new_condition:
            new_condition = ""
        # there are conditionals (same or different) so we must indent
        indent = base_indent + "\t"
    else:
        indent = base_indent
        new_condition = ""

    return indent, new_condition


class Union:
    def __init__(self, compound: 'Compound', union_name: str) -> None:
        self.compounds: 'Compound' = compound
        self.parser: 'XmlParser' = self.compounds.parser
        self.name: str = union_name
        self.members: list['Element'] = []
        self._params_cache: dict[tuple[int, str, bool], FieldParams] = {}

    def is_ovl_ptr(self) -> bool:
        """Check if this union is used as an ovl memory pointer"""
        return any(
            field.attrib.get("type", "") in ("Pointer", "ArrayPointer", "ForEachPointer")
            for field in self.members
        )

    def append(self, member: 'Element') -> None:
        self.members.append(member)

    def indirect_class_access(self, field_type: str) -> str:
        return f"name_type_map['{field_type}']"

    def is_type(self, potential_type: XmlType) -> bool:
        if isinstance(potential_type, str):
            if potential_type in self.compounds.parser.path_dict:
                return True
            if potential_type.startswith('name_type_map'):
                return True
        return False

    def get_conditions(self, field: 'Element', target_variable: str, use_abstract: bool = False) -> tuple[list[str], list[str]]:
        """Returns a list of conditional expressions for a field of this union"""
        CONTEXT = CONTEXT_SUFFIX if target_variable == '' else f'{target_variable}.{CONTEXT_SUFFIX}'
        VER = f"{CONTEXT}.version"
        global_conditionals: list[str] = []
        local_conditionals: list[str] = []

        # extract (formatted) field values
        ver1_str: XmlStr = self.parser.get_attr_with_backups(field, ["ver1", "since"])
        ver2_str: XmlStr = self.parser.get_attr_with_backups(field, ["ver2", "until"])
        vercond_str: XmlStr = field.attrib.get("vercond", None)
        ver1: Version | None = Version(ver1_str) if ver1_str else None
        ver2: Version | None = Version(ver2_str) if ver2_str else None
        vercond: XmlExpr = None
        valid_versions_str: XmlStr = field.attrib.get("versions", None)
        valid_versions = [Versions.format_id(version) for version in valid_versions_str.split(" ")] if valid_versions_str else None
        cond_str: XmlStr = field.attrib.get("cond", None)
        cond: XmlExpr = None
        onlyT: XmlStr = field.attrib.get("onlyT", None)
        excludeT: XmlStr = field.attrib.get("excludeT", None)

        # resolve the field values to python conditional expressions
        # global conditions
        if ver1 and ver2:
            global_conditionals.append(f"{ver1} <= {VER} <= {ver2}")
        elif ver1:
            global_conditionals.append(f"{VER} >= {ver1}")
        elif ver2:
            global_conditionals.append(f"{VER} <= {ver2}")
        # version condition on context
        if vercond_str:
            vercond = Expression(vercond_str, CONTEXT)
            global_conditionals.append(f"{vercond}")
        if valid_versions:
            global_conditionals.append(f"({' or '.join([f'versions.is_{version}({CONTEXT})' for version in valid_versions])})")

        # local conditions
        if cond_str:
            cond = Expression(cond_str, target_variable)
            local_conditionals.append(f"{cond}")
        if onlyT:
            onlyT = self.indirect_class_access(onlyT)
            local_conditionals.append(f"isinstance({target_variable}, {onlyT})")
        if excludeT:
            excludeT = self.indirect_class_access(excludeT)
            local_conditionals.append(f"not isinstance({target_variable}, {excludeT})")

        # technically neither, with local conditions for now
        if use_abstract:
            if field.attrib.get("abstract", "False") == "True":
                local_conditionals.append("include_abstract")
        return global_conditionals, local_conditionals

    def get_params(self, field: 'Element', target_variable: str = "self", use_abstract: bool = False) -> 'FieldParams':
        # parse all attributes and return the python-evaluatable string
        cache_key: tuple[int, str, bool] = (id(field), target_variable, use_abstract)
        if cache_key in self._params_cache:
            return self._params_cache[cache_key]

        field_name = field.attrib["name"]
        field_type = field.attrib["type"]
        if field_type == "template":
            field_type_access = f'{target_variable}.{field_type}'
        else:
            field_type_access = self.indirect_class_access(field_type)
        template = self.parser.get_attr_with_array_alt(field, "template")
        optional = field.attrib.get("optional", "False")
        default = field.attrib.get("default", None)

        conditionals = self.get_conditions(field, target_variable, use_abstract)

        arg: str | list[str] | None = self.parser.get_attr_with_array_alt(field, "arg")
        arr1_str: XmlStr = self.parser.get_attr_with_backups(field, ["arr1", "length"])
        arr2_str: XmlStr = self.parser.get_attr_with_backups(field, ["arr2", "width"])
        arr3_str: XmlStr = self.parser.get_attr_with_backups(field, ["arr3", "depth"])
        arr1: XmlExpr = Expression(arr1_str, target_variable) if arr1_str else None
        arr2: XmlExpr = Expression(arr2_str, target_variable) if arr2_str else None
        arr3: XmlExpr = Expression(arr3_str, target_variable) if arr3_str else None

        def format_template(template_entry: XmlStr) -> str | None:
            if not template_entry:
                return None
            # template can be either a type or a reference to a local field
            template_class: str = name_class(template_entry)
            if template_class not in self.compounds.parser.path_dict:
                return str(Expression(template_entry, target_variable))
            else:
                return self.indirect_class_access(template_class)

        processed_template: str | tuple[str | None, ...] | None
        if isinstance(template, list):
            processed_template = tuple(format_template(entry) for entry in template)
        else:
            processed_template = format_template(template)

        def format_arg(arg_entry: str) -> str | Expression:
            # allow accessing the instance directly as an argument
            if arg_entry in ("self", "instance", "#SELF#"):
                return target_variable
            else:
                return Expression(arg_entry, target_variable)

        processed_arg: str
        if isinstance(arg, list):
            processed_arg_parts = (format_arg(entry) for entry in arg)
            processed_arg = f"({', '.join(map(str, processed_arg_parts))})"
        elif arg is not None:
            processed_arg = str(format_arg(arg))
        else:
            processed_arg = "0"

        params = FieldParams(
            arg=processed_arg,
            template=processed_template,
            arrays=ArrayExprTuple((arr1, arr2, arr3)),
            conditionals=conditionals,
            name=field_name,
            field_type=field_type,
            field_type_access=field_type_access,
            optional=optional,
            default=default
        )
        self._params_cache[cache_key] = params
        return params

    def default_to_value(self, default_string: XmlStr, field_type: XmlStr, field_type_access: XmlStr) -> XmlStr:
        if not default_string:
            # don't convert None to string here
            return default_string
        if ", " in default_string:
            # already formatted by format_potential_tuple
            return default_string
        literal_value = interpret_literal(default_string)
        if literal_value is not None:
            return str(literal_value)
        if field_type:
            bool_value = self.parser.interpret_boolean(field_type, default_string)
            if bool_value is not None:
                return bool_value
        if field_type and field_type in self.parser.path_dict and self.parser.tag_dict[field_type.lower()] in ("enum", "bitflags"):
            enum_value = name_enum_key_if_necessary(default_string)
            return f'{field_type_access}.{enum_value}'
        # not interpretable in any way, must be a string
        return repr(default_string)

    def get_default_string(self, default_string: XmlStr, context: str, p: 'FieldParams') -> str:
        # get the default (or the best guess of it)
        if p.arrays[0]:
            # init with empty shape to work regardless of condition
            return f'Array({context}, {p.arg}, {p.template}, (0,), {p.field_type_access})'
        else:
            default_string = self.default_to_value(default_string, p.field_type, p.field_type_access)
            if default_string:
                if self.compounds.parser.tag_dict.get(p.field_type.lower()) == "enum":
                    # the default string, when evaluated, gives the correct type
                    return default_string
                else:
                    # the default string needs to be converted to an object of the proper type
                    return f'{p.field_type_access}.from_value({default_string})'
            else:
                # instantiate like a generic type: dtype(context, arg, template)
                return f'{p.field_type_access}({context}, {p.arg}, {p.template})'

    def _get_pyi_type_name(self, type_name: str) -> str:
        """Returns the appropriate name for a type in a .pyi file."""
        # Note: type_name is expected to be already capitalized by name_class if needed
        basics: Basics | None = self.parser.basics
        if not basics:
            return type_name
        if type_name in basics.booleans:
            return "bool"
        if type_name in basics.strings:
            return "str"
        if type_name in basics.integrals:
            return "int"
        if type_name in basics.floats:
            return "float"
        return type_name

    def get_type_hint(self, field: 'Element') -> str:
        """Generates a type hint string for a given field for .pyi files."""
        field_type_str: str = field.attrib["type"]
        field_type: str = name_class(field_type_str)  # Base type class name

        template: str | list[str] | None = self.parser.get_attr_with_array_alt(field, "template")
        arr1: XmlStr = self.parser.get_attr_with_backups(field, ["arr1", "length"])
        arr2: XmlStr = self.parser.get_attr_with_backups(field, ["arr2", "width"])
        arr3: XmlStr = self.parser.get_attr_with_backups(field, ["arr3", "depth"])
        allow_np: bool = field_type in self.parser.numpy_types
        # The type is `#T#`
        type_is_template: Match[str] | None = template_re.fullmatch(field_type_str)

        # The base type of the field
        field_type_hint: XmlStr = None
        if type_is_template:
            # type="#T#". The item type is simply the generic TypeVar
            field_type_hint = "_T"
        else:
            # A concrete type, which may or may not be templated
            template_type_hint = None
            if template:
                templates = template if isinstance(template, list) else [template]
                inner_type_str = templates[0]
                inner_type_class_name = name_class(inner_type_str)
                if inner_type_class_name in self.parser.path_dict:
                    template_type_hint = self._get_pyi_type_name(inner_type_class_name)
                else:
                    template_type_hint = "object"

            # Fallback for untemplated Pointers to default to Pointer[object]
            if field_type == "Pointer" and not template_type_hint:
                template_type_hint = "object"
            
            if template_type_hint:
                # This is a generic type, e.g., Pointer[ZString] -> "Pointer[str]"
                field_type_hint = f"{field_type}[{template_type_hint}]"
            else:
                # This is a simple non-generic type
                field_type_hint = self._get_pyi_type_name(field_type)

        # If it's an array, wrap the item type
        if arr1:
            array_hint: str = f"Array[{field_type_hint}]" if not allow_np else f"np.ndarray[tuple[int], np.dtype[{field_type_hint}]]"
            if arr2:
                array_hint = f"Array[{array_hint}]" if not allow_np else f"np.ndarray[tuple[int, int], np.dtype[{field_type_hint}]]"
            if arr3:
                array_hint = f"Array[{array_hint}]" if not allow_np else f"np.ndarray[tuple[int, int, int], np.dtype[{field_type_hint}]]"
            field_type_hint = array_hint

        return field_type_hint

    def write_init(self, f: TextIO) -> None:
        base_indent = "\t\t"
        debug_strs = []
        field_default = None
        for field in reversed(self.members):
            field_debug_str = clean_comment_str(field.text, indent=base_indent)
            params = self.get_params(field)
            if field_debug_str.strip() and field_debug_str not in debug_strs:
                debug_strs.append(field_debug_str)

            # we init each field with its basic default string so that the field exists regardless of any condition
            # by iterating in reverse, we use the last non-recursive field
            if field_default is None and not self.compounds.imports.is_recursive_field(field):
                field_default = self.get_default_string(
                    field.attrib.get('default', None), f'self.{CONTEXT_SUFFIX}', params)

        # add every (unique) debug string:
        for field_debug_str in reversed(debug_strs):
            f.write(field_debug_str)

        if field_default is not None:
            f.write(f'\n{base_indent}self.{params.name} = {field_default}')

    @staticmethod
    def arrs_to_tuple(arrays: ArrayExprTuple) -> str:
        valid_arrs = tuple(str(arr) for arr in arrays if arr)
        arr_str = f'({", ".join(valid_arrs)},)'
        return arr_str

    def write_attributes(self, f: TextIO) -> None:
        for field in self.members:
            params = self.get_params(field, "")

            # process arg
            try:
                arg_val: int | None = int(str(params.arg), 0)
            except (ValueError, TypeError):
                arg_val = None

            # process template
            template_val = params.template if self.is_type(params.template) else None

            # process field type
            field_type: XmlStr = params.field_type
            field_type_access: XmlStr = params.field_type_access
            if field_type not in self.parser.path_dict:
                field_type = None
                field_type_access = None

            default_val = self.default_to_value(params.default, field_type, field_type_access)

            # process arrays and arguments string
            if params.arrays[0] is None:
                arguments = f"({arg_val}, {template_val})"
            else:
                shape = self.arrs_to_tuple(params.arrays)
                shape_parts = shape[1:-1].split(",")
                resolved_shape_parts: list[str] = []
                for dim in shape_parts:
                    dim_str = dim.strip()
                    if dim_str:
                        try:
                            resolved_dim: int | None = int(dim_str, 0)
                        except ValueError:
                            resolved_dim = None
                        resolved_shape_parts.append(str(resolved_dim))
                shape_str = f"({', '.join(resolved_shape_parts)},)"
                arguments = f"({arg_val}, {template_val}, {shape_str}, {field_type_access})"
                field_type_access = "Array"

            # process conditionals
            global_conditions = f"lambda {CONTEXT_SUFFIX}: {' and '.join(params.conditionals[0])}" if params.conditionals[0] else None
            local_conditions = True if params.conditionals[1] else None

            f.write(
                f"\n\t\tyield {repr(params.name)}, {field_type_access}, {arguments}, ({params.optional}, {default_val}), ({global_conditions}, {local_conditions})"
            )


    def write_filtered_attributes(self, f: TextIO, condition: str, target_variable: str = "self") -> str:
        base_indent = "\n\t\t"
        for field in self.members:
            params = self.get_params(field, target_variable, use_abstract=True)
            field_type = params.field_type
            field_type_access = params.field_type_access
            default_val = self.default_to_value(params.default, field_type, field_type_access)

            if params.arrays[0] is None:
                arguments = f"({params.arg}, {params.template})"
            else:
                arguments = f"({params.arg}, {params.template}, {self.arrs_to_tuple(params.arrays)}, {field_type_access})"
                field_type_access = "Array"

            indent, new_condition = condition_indent(base_indent, params.conditionals, condition)
            if new_condition:
                f.write(f"{base_indent}{new_condition}")
            if new_condition or indent == base_indent:
                condition = new_condition

            default_children = field.findall("default")
            if default_children:
                condition_defaults: list[tuple[str, XmlStr]] = [(f'{indent}else:', default_val)]
                last_default = len(default_children) - 1
                def_condition = ""
                for i, default_element in enumerate(default_children):
                    # get the condition
                    conditionals = self.get_conditions(default_element, target_variable)
                    def_indent, new_def_condition = condition_indent(indent, conditionals, def_condition)
                    def_condition = new_def_condition
                    if not def_condition:
                        raise AttributeError(
                            f"Default tag without or with overlapping conditionals on {params.name} {def_condition} {default_element.get('value')}")
                    
                    def_keyword = "if" if i == 0 else "el"
                    def_line = f'{indent}{def_keyword}{def_condition[2:]}' # use slicing to remove "if"
                    
                    default_child_val = self.default_to_value(default_element.attrib.get("value", None), field_type, field_type_access)
                    condition_defaults.append((def_line, default_child_val))
                condition_defaults = condition_defaults[::-1]
            else:
                condition_defaults = [("", default_val)]

            for def_line, current_default in condition_defaults:
                def_indent = f'{indent}\t' if def_line else indent
                if def_line:
                    f.write(def_line)

                f.write(
                    f"{def_indent}yield {repr(params.name)}, {field_type_access}, {arguments}, ({params.optional}, {current_default})"
                )
        return condition
