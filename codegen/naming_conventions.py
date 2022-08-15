import re

# precompiled regular expressions, used in name_parts

_RE_NAME_SEP = re.compile('[_\W]+')
"""Matches seperators for splitting names."""

_RE_NAME_DIGITS = re.compile('([0-9]+)|([a-zA-Z]+)')
"""Matches digits or characters for splitting names."""

_RE_NAME_CAMEL = re.compile('([A-Z][a-z]*)|([a-z]+)')
"""Finds components of camelCase and CamelCase names."""

_RE_NAME_LC = re.compile('[a-z]')
"""Matches a lower case character."""

_RE_NAME_UC = re.compile('[A-Z]')
"""Matches an upper case character."""


def name_parts(name):
    """Intelligently split a name into parts:
    * first, split at non-alphanumeric characters
    * next, seperate digits from characters
    * finally, if some part has mixed case, it must be
      camel case so split it further at upper case characters
    >>> name_parts("hello_world")
    ['hello', 'world']
    >>> name_parts("HELLO_WORLD")
    ['HELLO', 'WORLD']
    >>> name_parts("HelloWorld")
    ['Hello', 'World']
    >>> name_parts("helloWorld")
    ['hello', 'World']
    >>> name_parts("xs:NMTOKEN")
    ['xs', 'NMTOKEN']
    >>> name_parts("xs:NCName")
    ['xs', 'N', 'C', 'Name']
    >>> name_parts('this IS a sillyNAME')
    ['this', 'IS', 'a', 'silly', 'N', 'A', 'M', 'E']
    >>> name_parts('tHis is A Silly naME')
    ['t', 'His', 'is', 'A', 'Silly', 'na', 'M', 'E']
    """
    # str(name) converts name to string in case it is a py2k
    # unicode string
    name = str(name)
    # separate at symbols
    parts = _RE_NAME_SEP.split(name)
    # seperate digits
    newparts = []
    for part in parts:
        for part_groups in _RE_NAME_DIGITS.findall(part):
            for group in part_groups:
                if group:
                    newparts.append(group)
                    break
    parts = newparts
    # separate at upper case characters for CamelCase and camelCase words
    newparts = []
    for part in parts:
        if _RE_NAME_LC.search(part) and _RE_NAME_UC.search(part):
            # find the camel bumps
            for part_groups in _RE_NAME_CAMEL.findall(part):
                for group in part_groups:
                    if group:
                        newparts.append(group)
                        break
        else:
            newparts.append(part)
    parts = newparts
    # return result
    return parts


def name_attribute(name):
    """Converts an attribute name, as in the description file,
    into a name usable by python.
    :param name: The attribute name.
    :type name: ``str``
    :return: Reformatted attribute name, useable by python.
    >>> name_attribute('tHis is A Silly naME')
    't_his_is_a_silly_na_m_e'
    >>> name_attribute('Test:Something')
    'test_something'
    >>> name_attribute('unknown?')
    'unknown'
    """
    prefix = "_" if name.startswith("_") else ""
    return prefix + '_'.join(part.lower() for part in name_parts(name))


def name_access(access):
    """Applies name_attribute to every part of a dot-separated string"""
    return '.'.join([name_attribute(attr) for attr in access.split('.')])


def name_class(name):
    """Converts a class name, as in the xsd file, into a name usable
    by python.
    :param name: The class name.
    :type name: str
    :return: Reformatted class name, useable by python.
    >>> name_class('this IS a sillyNAME')
    'ThisIsASillyNAME'
    """
    if name == "template":
        return name
    return ''.join(part.capitalize() for part in name_parts(name))


def name_enum_key(name):
    """Converts a key name into a name suitable for an enum key.
    :param name: the key name
    :type name: str
    :return: Reformatted key name.
    >>> name_enum_key('Some key name')
    'SOME_KEY_NAME'
    """
    return '_'.join(part.upper() for part in name_parts(name))


def name_enum_key_if_necessary(name):
    if len(name.split()) > 1 or name.upper() != name:
        return name_enum_key(name)
    else:
        return name


def clean_comment_str(comment_str="", indent="", class_comment=""):
    """Reformats an XML comment string into multi-line a python style comment block"""
    if comment_str is None:
        return ""
    if not comment_str.strip():
        return ""
    if class_comment:
        lines = [f"\n{indent}{class_comment}",] + [f"\n{indent}{line.strip()}" for line in comment_str.strip().split("\n")] + [f"\n{indent}{class_comment}",]
    else:
        lines = [f"\n{indent}# {line.strip()}" for line in comment_str.strip().split("\n")]
    return "\n" + "".join(lines)


def name_module(name):
    """Converts a module name into a name suitable for a python module
    :param name: the module name
    :type name: str
    :return: Reformatted module name
    >>> name_module('BSHavok')
    'bshavok'
    """
    return name.lower()


def str_is_number(str_expr):
    # check if it might be an int:
    try:
        int_value = int(str_expr, 0)
        return True
    except ValueError:
        # could still be a float
        try:
            float_value = float(str_expr)
            return True
        except ValueError:
            return False


def format_potential_tuple(value):
    """Converts xml attribute value lists to tuples if space is present and all
    space-separated values can be converted to numbers, otherwise leaves it alone.
    :param value: the string that is the value of an attribute
    :return: original string if no space is present, or commas as separators
    and surrounding parentheses if whitespace is present.
    >>> format_potential_tuple('1.0')
    '1.0
    >>> format_potential_tuple('1.0 1.0 1.0')
    '(1.0, 1.0, 1.0)'"""
    if ' ' in value:
        if all([str_is_number(potential_number) for potential_number in value.split()]):
            return f"({', '.join(value.split())})"
        else:
            return value
    else:
        return value


def force_bool(value):
    """Converts true/false or an integer to either 'True' or 'False'
    with all the usual rules of integer conversion to bools.
    :param value: the string to converts
    :return: 'True' or 'False' if the string converts to a bool, otherwise the original string
    >>> force_bool('0')
    'False'
    >>> force_bool('true')
    'True'
    >>> force_bool('some nonsense')
    'some nonsense'
    """
    bools = ("False", "True")
    capitalized = value.capitalize()
    if capitalized in bools:
        return capitalized
    else:
        try:
            int_value = int(value)
        except:
            return value
        return repr(bool(int_value))
