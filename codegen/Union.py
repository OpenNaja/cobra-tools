from itertools import chain

from codegen.expression import Expression, Version, interpret_literal
from codegen.Versions import Versions
import codegen.naming_conventions as convention

CONTEXT_SUFFIX = "context"


def condition_indent(base_indent, conditionals, condition=""):
    # determine the python condition and indentation level based on whether the
    # last used condition was the same.
    conditionals = tuple(chain.from_iterable(conditionals))
    if conditionals:
        new_condition = f"if {' and '.join(conditionals)}:"
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
    def __init__(self, compound, union_name):
        self.compounds = compound
        self.parser = self.compounds.parser
        self.name = union_name
        self.members = []

    def is_ovl_ptr(self):
        """Check if this union is used as an ovl memory pointer"""
        for field in self.members:
            arg, template, arr1, arr2, conditionals, field_name, (field_type, field_type_access), _ = self.get_params(field)
            if field_type in ("Pointer", "ArrayPointer", "ForEachPointer"):
                return True

    def append(self, member):
        self.members.append(member)

    def indirect_class_access(self, field_type):
        return f"name_type_map['{field_type}']"

    def is_type(self, potential_type):
        if isinstance(potential_type, str):
            if potential_type in self.compounds.parser.path_dict:
                return True
            if potential_type.startswith('name_type_map'):
                return True
        return False

    def get_conditions(self, field, target_variable, use_abstract=False):
        """Returns a list of conditional expressions for a field of this union"""
        CONTEXT = CONTEXT_SUFFIX if target_variable == '' else f'{target_variable}.{CONTEXT_SUFFIX}'
        VER = f"{CONTEXT}.version"
        global_conditionals = []
        local_conditionals = []

        # extract (formatted) field values
        ver1 = self.parser.get_attr_with_backups(field, ["ver1", "since"])
        if ver1:
            ver1 = Version(ver1)
        ver2 = self.parser.get_attr_with_backups(field, ["ver2", "until"])

        if ver2:
            ver2 = Version(ver2)
        vercond = field.attrib.get("vercond")
        valid_versions = field.attrib.get("versions")
        if valid_versions:
            valid_versions = [Versions.format_id(version) for version in valid_versions.split(" ")]
        cond = field.attrib.get("cond")
        onlyT = field.attrib.get("onlyT")
        excludeT = field.attrib.get("excludeT")

        # resolve the field values to python conditional expressions
        # global conditions
        if ver1 and ver2:
            global_conditionals.append(f"{ver1} <= {VER} <= {ver2}")
        elif ver1:
            global_conditionals.append(f"{VER} >= {ver1}")
        elif ver2:
            global_conditionals.append(f"{VER} <= {ver2}")
        # version condition on context
        if vercond:
            vercond = Expression(vercond, CONTEXT)
            global_conditionals.append(f"{vercond}")
        if valid_versions:
            global_conditionals.append(f"({' or '.join([f'versions.is_{version}({CONTEXT})' for version in valid_versions])})")

        # local conditions
        if cond:
            cond = Expression(cond, target_variable)
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

    def get_params(self, field, target_variable="self", use_abstract=False):
        # parse all attributes and return the python-evaluatable string

        field_name = field.attrib["name"]
        field_type = field.attrib["type"]
        if field_type == "template":
            field_type_access = f'{target_variable}.{field_type}'
        else:
            field_type_access = self.indirect_class_access(field_type)
        template = self.parser.get_attr_with_array_alt(field, "template")
        optional = (field.attrib.get("optional", "False"), field.attrib.get("default"))

        conditionals = self.get_conditions(field, target_variable, use_abstract)

        arg = self.parser.get_attr_with_array_alt(field, "arg")
        arr1 = self.parser.get_attr_with_backups(field, ["arr1", "length"])
        arr2 = self.parser.get_attr_with_backups(field, ["arr2", "width"])
        def format_template(template_entry):
            if template_entry:
                # template can be either a type or a reference to a local field
                template_class = convention.name_class(template_entry)
                if template_class not in self.compounds.parser.path_dict:
                    template_entry = Expression(template_entry, target_variable)
                else:
                    template_entry = self.indirect_class_access(template_class)
            return template_entry
        if isinstance(template, list):
            template = tuple(format_template(entry) for entry in template)
        else:
            template = format_template(template)

        def format_arg(arg_entry):
            if arg_entry is not None:
                # allow accessing the instance directly as an argument
                if arg_entry in ("self", "instance", "#SELF#"):
                    arg_entry = target_variable
                else:
                    # todo - somwhere along the line, some (?) arg_entry had been converted to an expression
                    if not isinstance(arg_entry, Expression):
                        arg_entry = Expression(arg_entry, target_variable)
            return arg_entry

        if isinstance(arg, list):
            arg = tuple(format_arg(entry) for entry in arg)
            # we don't want to have special names (eg. target_variable) print as strings
            arg = f"({', '.join(str(format_arg(entry)) for entry in arg)})"
        elif arg is not None:
            arg = format_arg(arg)
        else:
            arg = "0"

        if arr1:
            arr1 = Expression(arr1, target_variable)
        if arr2:
            arr2 = Expression(arr2, target_variable)
        return arg, template, arr1, arr2, conditionals, field_name, (field_type, field_type_access), optional

    def default_to_value(self, default_string, field_type, field_type_access):
        if default_string:
            if field_type in self.compounds.parser.path_dict and self.compounds.parser.tag_dict[field_type.lower()] == "enum":
                default_string = convention.name_enum_key_if_necessary(default_string)
                return f'{field_type_access}.{default_string}'
            else:
                if ", " in default_string:
                    # already formatted by format_potential_tuple
                    pass
                else:
                    # check for boolean
                    if field_type in self.compounds.parser.path_dict and \
                    self.compounds.parser.tag_dict[field_type.lower()] == "basic" and \
                        field_type in self.compounds.parser.basics.booleans:
                        # boolean basics *can* be used as booleans, but don't have to be
                        if default_string.capitalize() in ("True", "False"):
                            default_string = default_string.capitalize()
                            return default_string
                    value = interpret_literal(default_string)
                    if value is not None:
                        default_string = str(value)
                    else:
                        # not interpretable, must be a string
                        default_string = repr(default_string)
        return default_string

    def get_default_string(self, default_string, context, arg, template, arr1, field_type, field_type_access):
        # get the default (or the best guess of it)
        field_type_lower = field_type.lower()
        tag_of_field_type = self.compounds.parser.tag_dict.get(field_type_lower)
        default_string = self.default_to_value(default_string, field_type, field_type_access)

        if arr1:
            # init with empty shape to work regardless of condition
            return f'Array({context}, {arg}, {template}, (0,), {field_type_access})'
        else:
            if default_string:
                if tag_of_field_type == "enum":
                    # the default string, when evaluated, gives the correct type
                    return default_string
                else:
                    # the default sring needs to be converted to an object of the proper type
                    return f'{field_type_access}.from_value({default_string})'
            else:
                # instantiate like a generic type: dtype(context, arg, template)
                return f'{field_type_access}({context}, {arg}, {template})'

    def write_init(self, f):
        base_indent = "\t\t"
        debug_strs = []
        field_default = None
        for field in reversed(self.members):
            field_debug_str = convention.clean_comment_str(field.text, indent=base_indent)
            arg, template, arr1, arr2, conditionals, field_name, (field_type, field_type_access), _ = self.get_params(field)

            if field_debug_str.strip() and field_debug_str not in debug_strs:
                debug_strs.append(field_debug_str)

            # we init each field with its basic default string so that the field exists regardless of any condition
            # by iterating in reverse, we use the last non-recursive field
            if field_default is None and not self.compounds.imports.is_recursive_field(field):
                field_default = self.get_default_string(field.attrib.get('default'), f'self.{CONTEXT_SUFFIX}', arg, template,
                                                        arr1, field_type, field_type_access)

        # add every (unique) debug string:
        for field_debug_str in reversed(debug_strs):
            f.write(field_debug_str)

        if field_default is not None:
            f.write(f'\n{base_indent}self.{field_name} = {field_default}')

    @staticmethod
    def arrs_to_tuple(*args):
        valid_arrs = tuple(str(arr) for arr in args if arr)
        arr_str = f'({", ".join(valid_arrs)},)'
        return arr_str

    def write_attributes(self, f):
        for field in self.members:
            arg, template, arr1, arr2, (global_conditionals, local_conditionals), field_name, (field_type, field_type_access), (optional, default) = self.get_params(field, '')
            # replace all non-static values with None for now
            try:
                if isinstance(arg, tuple):
                    arg = tuple(int(str(entry), 0) for entry in arg)
                else:
                    arg = int(str(arg), 0)
            except ValueError:
                arg = None
            if isinstance(template, tuple):
                template = tuple(entry if self.is_type(entry) else None for entry in template)
                if any(entry is None for entry in template):
                    template = None
            else:
                template = template if self.is_type(template) else None
            if not self.is_type(template):
                template = None
            if field_type not in self.compounds.parser.path_dict:
                field_type = None
                field_type_access = None
            default = self.default_to_value(default, field_type, field_type_access)
            if arr1 is None:
                arguments = f"({arg}, {template})"
            else:
                shape = self.arrs_to_tuple(arr1, arr2)
                shape_parts = shape[1:-1].split(",")
                resolved_shape_parts = []
                for dim in shape_parts:
                    dim = dim.strip()
                    if dim:
                        try:
                            dim = int(dim, 0)
                        except ValueError:
                            dim = None
                        resolved_shape_parts.append(str(dim))
                shape = f"({', '.join(resolved_shape_parts)},)"
                arguments = f"({arg}, {template}, {shape}, {field_type_access})"
                field_type_access = "Array"
            global_conditions = f"lambda {CONTEXT_SUFFIX}: {' and '.join(global_conditionals)}" if global_conditionals else None
            local_conditions = True if local_conditionals else None
            f.write(f"\n\t\tyield {repr(field_name)}, {field_type_access}, {arguments}, ({optional}, {default}), ({global_conditions}, {local_conditions})")

    def write_filtered_attributes(self, f, condition, target_variable="self"):
        base_indent = "\n\t\t"
        for field in self.members:
            arg, template, arr1, arr2, conditionals, field_name, (field_type, field_type_access), (optional, default) = self.get_params(field, target_variable, use_abstract=True)
            default = self.default_to_value(default, field_type, field_type_access)
            if arr1 is None:
                arguments = f"({arg}, {template})"
            else:
                arguments = f"({arg}, {template}, {self.arrs_to_tuple(arr1, arr2)}, {field_type_access})"
                field_type_access = "Array"

            indent, new_condition = condition_indent(base_indent, conditionals, condition)
            if new_condition:
                f.write(f"{base_indent}{new_condition}")
            if new_condition or indent == base_indent:
                condition = new_condition

            default_children = field.findall("default")
            if default_children:

                condition_defaults = [(f'{indent}else:', default)]
                last_default = len(default_children) - 1
                def_condition = ""
                for i, default_element in enumerate(default_children):
    
                    # get the condition
                    conditionals = self.get_conditions(default_element, target_variable)
                    def_indent, def_condition = condition_indent(indent, conditionals, def_condition)
                    if not def_condition:
                        raise AttributeError(
                            f"Default tag without or with overlapping conditionals on {field.attrib['name']} {def_condition} {default_element.get('value')}")
                    if i != last_default:
                        def_condition = f'{indent}el{def_condition}'
                    else:
                        def_condition = f'{indent}{def_condition}'
                    condition_defaults.append((def_condition, self.default_to_value(default_element.attrib.get("value"), field_type, field_type_access)))
                condition_defaults = condition_defaults[::-1]
            else:
                condition_defaults = [("", default)]

            for def_condition, default in condition_defaults:
                if def_condition:
                    f.write(def_condition)
                    def_indent = f'{indent}\t'
                else:
                    def_indent = indent
                f.write(f"{def_indent}yield {repr(field_name)}, {field_type_access}, {arguments}, ({optional}, {default})")
        return condition
