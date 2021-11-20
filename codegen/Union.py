from codegen.expression import Expression, Version
from codegen.Versions import Versions
from .naming_conventions import clean_comment_str

CONTEXT = "self.context"
VER = f"{CONTEXT}.version"


def get_attr_with_backups(field, attribute_keys):
    # return the value of the first attribute in the list that is not empty or
    # missing
    for key in attribute_keys:
        attr_value = field.attrib.get(key)
        if attr_value:
            return attr_value
    else:
        return None


def get_conditions(field):
    conditionals = []
    ver1 = get_attr_with_backups(field, ["ver1", "since"])
    if ver1:
        ver1 = Version(ver1)
    ver2 = get_attr_with_backups(field, ["ver2", "until"])

    if ver2:
        ver2 = Version(ver2)
    vercond = field.attrib.get("vercond")
    valid_versions = field.attrib.get("versions")
    if valid_versions:
        valid_versions = [Versions.format_id(version) for version in valid_versions.split(" ")]
    cond = field.attrib.get("cond")
    onlyT = field.attrib.get("onlyT")
    excludeT = field.attrib.get("excludeT")
    if ver1 and ver2:
        conditionals.append(f"{ver1} <= {VER} <= {ver2}")
    elif ver1:
        conditionals.append(f"{VER} >= {ver1}")
    elif ver2:
        conditionals.append(f"{VER} <= {ver2}")
    if vercond:
        vercond = Expression(vercond, g_vars=True)
        conditionals.append(f"{vercond}")
    if valid_versions:
        conditionals.append(f"({' or '.join([f'versions.is_{version}({CONTEXT})' for version in valid_versions])})")
    if cond:
        cond = Expression(cond)
        conditionals.append(f"{cond}")
    if onlyT:
        conditionals.append(f"'{onlyT}' in [parent.__name__ for parent in type(self).__mro__]")
    if excludeT:
        conditionals.append(f"'{excludeT}' not in [parent.__name__ for parent in type(self).__mro__]")
    return conditionals


def get_params(field):
    # parse all attributes and return the python-evaluatable string

    field_name = field.attrib["name"]
    field_type = field.attrib["type"]
    pad_mode = field.attrib.get("padding")
    template = field.attrib.get("template")

    conditionals = get_conditions(field)

    arg = field.attrib.get("arg")
    arr1 = get_attr_with_backups(field, ["arr1", "length"])
    arr2 = get_attr_with_backups(field, ["arr2", "width"])
    if arg:
        arg = Expression(arg)
    if arr1:
        arr1 = Expression(arr1)
    if arr2:
        arr2 = Expression(arr2)
    return arg, template, arr1, arr2, conditionals, field_name, field_type, pad_mode


def condition_indent(base_indent, conditionals, condition=""):
    # determine the python condition and indentation level based on whether the
    # last used condition was the same.
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
        self.compound = compound
        self.name = union_name
        self.members = []

    def append(self, member):
        self.members.append(member)

    def get_default_string(self, default_string, arg, template, arr1, arr2, field_name, field_type):
        # get the default (or the best guess of it)
        field_type_lower = field_type.lower()
        tag_of_field_type = self.compound.parser.tag_dict.get(field_type_lower)
        _, return_type = self.compound.parser.map_type(field_type, arr1)
        if tag_of_field_type == "enum" and default_string:
            default_string = f'{field_type}.{default_string}'

        if arr1:
            valid_arrs = tuple(str(arr) for arr in (arr1, arr2) if arr and ".arg" not in str(arr))
            arr_str = f'({", ".join(valid_arrs)})'
            if default_string:
                if return_type[0] == 'numpy':
                    return f'numpy.full({arr_str}, dtype={return_type[1]}, fill_value={default_string})'
                else:
                    return f'Array.from_value({arr_str}, {field_type}, {default_string})'
            else:
                if return_type[0] == 'numpy':
                    return f'numpy.zeros({arr_str}, dtype={return_type[1]})'
                else:
                    return f'Array({arr_str}, {field_type}, {CONTEXT}, {arg}, {template})'
        else:
            if default_string:
                if return_type in self.compound.parser.builtin_literals or tag_of_field_type == "enum":
                    # the default string, when evaluated, gives the correct type
                    return default_string
                else:
                    # the default sring needs to be converted to an object of the proper type
                    return f'{field_type}.from_value({default_string})'
            else:
                # we don't have a specified default, guess one
                if return_type in self.compound.parser.builtin_literals:
                    # this type can be returned from a literal
                    return repr(self.compound.parser.builtin_literals[return_type])
                else:
                    # instantiate like a generic type: dtype(context, arg, template)
                    return f'{field_type}({CONTEXT}, {arg}, {template})'


    def default_assigns(self, field, arg, template, arr1, arr2, field_name, field_type, base_indent):
        field_default = self.get_default_string(field.attrib.get('default'), arg, template, arr1, arr2, field_name,
                                                field_type)
        default_children = field.findall("default")
        if default_children:
            defaults = [(f'{base_indent}else:', f'{base_indent}\tself.{field_name} = {field_default}')]
            last_default = len(default_children) - 1
            condition = ""
            for i, default_element in enumerate(default_children):

                # get the condition
                conditionals = get_conditions(default_element)
                indent, condition = condition_indent(base_indent, conditionals, condition)
                if not condition:
                    raise AttributeError(
                        f"Default tag without or with overlapping conditionals on {field.attrib['name']} {condition} {default_element.get('value')}")
                if i != last_default:
                    condition = f'{base_indent}el{condition}'
                else:
                    condition = f'{base_indent}{condition}'

                default = self.get_default_string(default_element.attrib.get("value"), arg, template, arr1, arr2,
                                                  field_name, field_type)
                defaults.append((condition, f'{indent}self.{field_name} = {default}'))

            defaults = defaults[::-1]
        else:
            defaults = [("", f'{base_indent}self.{field_name} = {field_default}')]
        return defaults

    def write_init(self, f):
        base_indent = "\n\t\t"
        for field in self.members:
            field_debug_str = clean_comment_str(field.text, indent="\t\t")
            arg, template, arr1, arr2, conditionals, field_name, field_type, pad_mode = get_params(field)
            if field_debug_str.strip():
                f.write(field_debug_str)

            # we init each field with its basic default string so that the field exists regardless of any condition
            field_default = self.get_default_string(field.attrib.get('default'), arg, template, arr1, arr2, field_name,
                                                    field_type)
            f.write(f'{base_indent}self.{field_name} = {field_default}')

    def write_defaults(self, f, condition=""):
        base_indent = "\n\t\t"
        for field in self.members:
            arg, template, arr1, arr2, conditionals, field_name, field_type, pad_mode = get_params(field)

            indent, condition = condition_indent(base_indent, conditionals, condition)

            defaults = self.default_assigns(field, arg, template, arr1, arr2, field_name, field_type, indent)

            # if defaults:
            if condition:
                f.write(f"{base_indent}{condition}")
            for condition, default in defaults:
                if condition:
                    f.write(condition)
                f.write(default)
        return condition

    def write_io(self, f, method_type, condition=""):
        base_indent = "\n\t\t"
        for field in self.members:
            arg, template, arr1, arr2, conditionals, field_name, field_type, pad_mode = get_params(field)
            indent, condition = condition_indent(base_indent, conditionals, condition)
            if condition:
                f.write(f"{base_indent}{condition}")
            if arr1:
                if self.compound.parser.tag_dict[field_type.lower()] == "basic":
                    valid_arrs = tuple(str(arr) for arr in (arr1, arr2) if arr)
                    arr_str = ", ".join(valid_arrs)
                    if method_type == "read":
                        f.write(f"{indent}self.{field_name} = stream.{method_type}_{field_type.lower()}s(({arr_str}))")
                    else:
                        if pad_mode:
                            # resize numpy arrays that represent padding so we need not worry about them
                            f.write(f"{indent}self.{field_name}.resize(({arr_str}))")
                        f.write(f"{indent}stream.{method_type}_{field_type.lower()}s(self.{field_name})")
                else:
                    f.write(f"{indent}self.{field_name}.{method_type}(stream, {field_type}, {arr1}, {arr2})")
            else:
                f.write(
                    f"{indent}{self.compound.parser.method_for_type(field_type, mode=method_type, attr=f'self.{field_name}', arg=arg, template=template)}")
            if method_type == 'read':
                # store version related fields on self.context on read
                for k, (access, dtype) in self.compound.parser.verattrs.items():
                    # check all version-related global variables registered with the verattr tag
                    attr_path = access.split('.')
                    if field_name == attr_path[0]:
                        if dtype is None or len(attr_path) > 1 or field_type == dtype:
                            # the verattr type isn't known, we can't check it or it matches
                            f.write(f"{indent}{CONTEXT}.{field_name} = self.{field_name}")
                            break
        return condition
