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
    return '_'.join(part.lower() for part in name_parts(name))


def name_class(name):
    """Converts a class name, as in the xsd file, into a name usable
    by python.
    :param name: The class name.
    :type name: str
    :return: Reformatted class name, useable by python.
    >>> name_class('this IS a sillyNAME')
    'ThisIsASillyNAME'
    """
    if name == "self.template":
        return name
    return ''.join(part.capitalize() for part in name_parts(name))


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