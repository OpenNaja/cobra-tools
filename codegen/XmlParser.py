import logging
import os
import re
import itertools
from html import unescape
from typing import Callable, Iterable, TextIO, TYPE_CHECKING, Any, assert_type
if TYPE_CHECKING:
    from . import ElementTree, Element

from . import Config, XmlGenerationError, ET, LXML_INSTALLED, XMLSCHEMA_INSTALLED
from .Basics import Basics
from .Compound import Compound
from .Enum import Enum
from .Bitfield import Bitfield
from .Versions import Versions
from .Module import Module
from .naming_conventions import (force_bool, name_access, name_attribute, name_class,
                                 name_enum_key_if_necessary, name_module, clean_comment_str, template_re)
from .path_utils import module_path_to_import_path, module_path_to_file_path, to_import_path, pluralize_name
from .expression import format_potential_tuple


arg_regex = re.compile(r"(#ARG)([0-9]*)(#)")
template_regex = re.compile(r"(#T)([0-9]*)(#)")


class XmlParser:
    struct_types = ("compound", "niobject", "struct")
    bitstruct_types = ("bitfield", "bitflags", "bitstruct")
    builtin_literals = {'str': '', 'float': 0.0, 'int': 0, 'bool': False}

    def __init__(self, format_name: str, cfg: Config, path_dict: dict[str, str] | None = None) -> None:
        """Set up the xml parser."""
        self.format_name: str = format_name
        self.config: Config = cfg
        self.root_dir: str = cfg.root_dir
        self.gen_dir: str = cfg.gen_dir
        self.src_dir: str = cfg.src_dir
        self.write_stubs: bool = cfg.write_stubs
        self.base_segments: str = os.path.join("formats", self.format_name)
        # which encoding to use for the output files
        self.encoding = 'utf-8'

        # Store the root element
        self.root: Element| None = None

        # elements for versions
        self.versions: 'Versions' | None = None

        # ordered (!) list of tuples ({tokens}, (target_attribs)) for each <token>
        self.tokens: list[tuple[list[tuple[str, str]], list[str]]] = []

        # maps version attribute name to [access, type]
        self.verattrs: dict[str, list[str | None]] = {}
        # maps each type to its generated py file's relative path
        self.path_dict = {
            "Array": "array",
            "BasicBitfield": "bitfield",
            "BitfieldMember": "bitfield",
            "versions": self.base_segments,
            "ContextReference": "context",
            "BaseEnum": "base_enum",
            "BaseStruct": "base_struct",
            "name_type_map": os.path.join(self.base_segments, "imports")
        }
        if path_dict:
            self.path_dict.update(path_dict)
        # maps each type to its member tag type
        self.tag_dict: dict[str, str] = {}
        # order is relevant to ensure that structs are later imported in the correct order in generated code
        self.processed_types: dict[str, None] = {}

        self.basics: 'Basics' | None = None
        self.generic_types: set[str] = set(["Pointer", "ArrayPointer", "ForEachPointer"])
        self.numpy_types: set[str] = set()

        # Create a lookup dictionary for attribute-specific tokens. This provides fast O(1) access.
        self.token_map = {
            target_attrib: tokens
            for tokens, target_attribs in self.tokens
            for target_attrib in target_attribs
        }

        # Define fixed replacements and pre-compile regexes
        self.fixed_tokens = (("\\", "."), ("#SELF#", "instance"))
        fixed_array_parts = ((arg_regex, "arg"), (template_regex, "template"))
        self.compiled_regexes = [
            (re.compile(pattern), self.match_replace_function(base))
            for pattern, base in fixed_array_parts
        ]

    def process(self, root: 'Element', xml_path: str, parsed_xmls: dict[str, 'XmlParser']) -> None:
        """preprocessing - generate module paths for imports relative to the output dir"""
        for child in root:
            if not isinstance(child.tag, str):
                continue

            if child.tag == "token":
                # tokens must be applied before applying naming conventions
                self.read_token(child)
                continue
            elif child.tag.split('}')[-1] == "include":
                # xinclude element which may include tokens, read the element to add them
                self.read_xinclude(child, xml_path, parsed_xmls)
                continue
            self.replace_tokens(child)
            self.apply_conventions(child)

            # only check stuff that has a name - ignore version tags
            if child.tag.split('}')[-1] not in ("version", "token", "include", "verattr"):
                class_name = child.attrib["name"]
                base_segments = self.base_segments

                # Determine the base path (respecting the 'module' attribute)
                if child.tag not in ("module", "basic") and child.attrib.get("module"):
                    base_segments = self.path_dict[child.attrib["module"]]

                # store the final relative module path for this class
                self.path_dict[class_name] = os.path.join(base_segments, *self.get_class_path_segments(child))
                self.tag_dict[class_name.lower()] = child.tag
            
            # Pre-scan to find types used with templates and generic definitions
            if child.tag in self.struct_types:
                for field in child:
                    # This is the existing "usage" check
                    if field.tag in ("add", "field") and "template" in field.attrib:
                        self.generic_types.add(name_class(field.attrib["type"]))

                    template = self.get_attr_with_array_alt(field, "template")
                    field_type = field.attrib.get("type")
                    is_gen_template = template and isinstance(template, str) and template_re.fullmatch(template)
                    is_gen_type = field_type and template_re.fullmatch(field_type)
                    if is_gen_template or is_gen_type:
                        # This class is generic by its own definition. Register it.
                        self.generic_types.add(child.attrib["name"])
                        break # Found a generic field, no need to check others in this class

            try:
                if child.tag in self.struct_types:
                    Compound(self, child, self.config)
                elif child.tag in self.bitstruct_types:
                    Bitfield(self, child, self.config)
                elif child.tag == "basic":
                    self.basics.read(child)
                elif child.tag == "enum":
                    Enum(self, child, self.config)
                elif child.tag == "module":
                    Module(self, child, self.gen_dir, self.root_dir)
                elif child.tag == "version":
                    self.versions.read(child)
                elif child.tag == "verattr":
                    self.read_verattr(child)
            except Exception as e:
                logging.exception(f"Parsing child {child} failed")
                raise XmlGenerationError(f"Failed to process child {child.tag} with name '{child.attrib.get('name')}'.") from e



    def load_xml(self, xml_file: str | TextIO, parsed_xmls: dict[str, 'XmlParser'] | None = None) -> None:
        """Loads an XML (can be filepath or open file) and does all parsing
        Goes over all children of the root node and calls the appropriate function depending on type of the child"""

        if isinstance(xml_file, str):
            xml_path = xml_file
        else:
            xml_path = xml_file.name
        xml_path = os.path.realpath(xml_path)
        # dictionary of xml file: XmlParser
        if parsed_xmls is None:
            parsed_xmls = {}

        tree: ElementTree | None = None
        if LXML_INSTALLED and ET:
            # Use lxml if available
            parser = ET.XMLParser(remove_blank_text=True)
            tree = ET.parse(xml_path, parser)
            self.root = tree.getroot()
        else:
            # Fallback to the standard library's ElementTree
            tree = ET.parse(xml_path)
            self.root = tree.getroot()
        
        self.versions = Versions(self, gen_dir=self.gen_dir)
        self.basics = Basics(self)

        self.process(self.root, xml_path, parsed_xmls)

        versions_file = module_path_to_file_path(os.path.join(self.base_segments, "versions"), self.gen_dir, self.root_dir)
        self.versions.write(versions_file)
        imports_module = os.path.join(self.base_segments, "imports")
        self.write_import_map(module_path_to_file_path(imports_module, self.gen_dir, self.root_dir))
        init_file_path = module_path_to_file_path(os.path.join(self.base_segments, "__init__"), self.gen_dir, self.root_dir)
        import_string = f'from {module_path_to_import_path(imports_module, self.gen_dir)} import name_type_map\n'
        if not os.path.exists(init_file_path):
            with open(init_file_path, "w", encoding=self.encoding) as f:
                f.write(import_string)
        else:
            # If the file exists, read its content first.
            with open(init_file_path, "r+", encoding=self.encoding) as f:
                init_content = f.read()
                # Only modify the file if the import string is NOT already present.
                if import_string.strip() not in init_content:
                    f.seek(0, 0) # Rewind to the beginning of the file.
                    f.write(import_string)
                    f.write(init_content)

        parsed_xmls[xml_path] = self

    def write_import_map(self, file: str) -> None:
        with open(file, "w", encoding=self.encoding) as f:
            f.write("from importlib import import_module\n")
            f.write("\n\ntype_module_name_map = {\n")
            for type_name in self.processed_types:
                f.write(f"\t'{type_name}': '{module_path_to_import_path(self.path_dict[type_name], self.gen_dir)}',\n")
            f.write('}\n')
            f.write("\nname_type_map = {}\n")
            f.write("for type_name, module in type_module_name_map.items():\n")
            f.write("\tname_type_map[type_name] = getattr(import_module(module), type_name)\n")
            f.write("for class_object in name_type_map.values():\n")
            f.write("\tif callable(getattr(class_object, 'init_attributes', None)):\n")
            f.write("\t\tclass_object.init_attributes()\n")

    # the following constructs do not create classes
    def read_token(self, token: 'Element') -> None:
        """Reads an xml <token> block and stores it in the tokens list"""
        self.tokens.append(([(sub_token.attrib["token"], sub_token.attrib["string"])
                            for sub_token in token if isinstance(sub_token.tag, str)],
                            token.attrib["attrs"].split(" ")))

    def read_verattr(self, verattr: 'Element') -> None:
        """Reads an xml <verattr> and stores it in the verattrs dict"""
        name = verattr.attrib['name']
        assert name not in self.verattrs, f"verattr {name} already defined!"
        access = verattr.attrib['access']
        attr_type = verattr.attrib.get('type')
        self.verattrs[name] = [access, attr_type]

    def read_xinclude(self, xinclude: 'Element', xml_path: str, parsed_xmls: dict[str, 'XmlParser']) -> None:
        """Reads an xi:include element, and parses the linked xml if it doesn't exist yet in parsed xmls"""
        # convert the linked relative path to an absolute one
        new_path = os.path.realpath(os.path.join(os.path.dirname(xml_path), xinclude.attrib['href']))
        # check if the xml file was already parsed
        if new_path not in parsed_xmls:
            # if not, parse it now
            format_name = os.path.splitext(os.path.basename(new_path))[0]
            new_parser = XmlParser(format_name, self.config)
            new_parser.load_xml(new_path, parsed_xmls)
        else:
            new_parser = parsed_xmls[new_path]
        # append all pertinent information (file paths etc) to self for access
        self.copy_xml_dicts(new_parser)

    @staticmethod
    def apply_convention(struct: 'Element', func: Callable[[str], str], params: Iterable[str]) -> None:
        for k in params:
            if struct.attrib.get(k):
                struct.attrib[k] = func(struct.attrib[k])

    def apply_conventions(self, struct: 'Element') -> None:
        # Prevent this from ever running on certain tags
        if struct.tag in ('{http://www.w3.org/2001/XInclude}include',):
            return
        # struct top level
        if struct.tag in ("token",):
            # don't apply conventions to these types (or there are none to apply)
            return
        elif struct.tag == "version":
            self.apply_convention(struct, force_bool, ("supported", "custom"))
        elif struct.tag == "verattr":
            self.apply_convention(struct, name_class, ("type",))
            self.apply_convention(struct, name_access, ("access",))
        elif struct.tag == "module":
            self.apply_convention(struct, name_module, ("name", "depends"))
            self.apply_convention(struct, force_bool, ("custom",))
            struct.text = clean_comment_str(struct.text, indent="", class_comment='"""')[2:]
        else:
            # Conventions for any class-like elements
            if "name" in struct.attrib:
                # If "name" doesn't exist at this point, XSD Schema will catch and report it
                struct.attrib["__name__"] = struct.attrib["name"]
            self.apply_convention(struct, name_class, ("name", "inherit"))
            self.apply_convention(struct, name_module, ("module",))
            if struct.tag == "basic":
                self.apply_convention(struct, force_bool, ("boolean", "integral", "countable", "generic"))
            elif struct.tag == "enum":
                self.apply_convention(struct, name_class, ("storage",))
                for option in struct:
                    self.apply_convention(option, name_enum_key_if_necessary, ("name", ))
            elif struct.tag in self.bitstruct_types:
                self.apply_convention(struct, name_class, ("storage",))
                # a bitfield/bitflags fields
                if struct.tag == 'bitflags':
                    for field in struct:
                        field.attrib['enum_name'] = name_enum_key_if_necessary(field.attrib['name'])
                for field in struct:
                    self.apply_convention(field, name_attribute, ("name",))
                    self.apply_convention(field, name_class, ("type",))
            elif struct.tag in self.struct_types:
                self.apply_convention(struct, force_bool, ("generic",))
                self.apply_convention(struct, force_bool, ("allow_np",))
                if struct.attrib.get("allow_np"):
                    self.numpy_types.add(struct.attrib["name"])
                # a struct's fields
                for field in struct:
                    self.apply_convention(field, name_attribute, ("name",))
                    self.apply_convention(field, name_class, ("type", "onlyT", "excludeT"))
                    self.apply_convention(field, force_bool, ("optional", "abstract", "recursive"))
                    # template can refer to a type of an attribute
                    self.apply_convention(field, format_potential_tuple, ("default",))
                    for default in field:
                        self.apply_convention(default, name_class, ("onlyT",))
                        self.apply_convention(default, format_potential_tuple, ("value",))
            # filter comment str
            struct.text = clean_comment_str(struct.text, indent="\t", class_comment='"""')

    @staticmethod
    def match_replace_function(base_string: str) -> Callable[[re.Match[str]], str]:
        def match_replace(match_object: re.Match[str]) -> str:
            if match_object.group(2):
                indexing = f'_{match_object.group(2)}'
            else:
                indexing = ''
            return f'{base_string}{indexing}'
        return match_replace

    def replace_tokens(self, xml_struct: 'Element') -> None:
        """Update xml_struct's (and all of its children's) attrib dict with content of tokens+versions list."""
        # replace versions after tokens because tokens include versions
        for tokens, target_attribs in self.tokens:
            for target_attrib in target_attribs:
                if target_attrib in xml_struct.attrib:
                    expr_str = xml_struct.attrib[target_attrib]
                    for op_token, op_str in tokens:
                        expr_str = expr_str.replace(op_token, op_str)
                    # get rid of any remaining html escape characters
                    xml_struct.attrib[target_attrib] = unescape(expr_str)
        for attrib, expr_str in xml_struct.attrib.items():
            for op_token, op_str in self.fixed_tokens:
                expr_str = expr_str.replace(op_token, op_str)
            for pattern, repl_func in self.compiled_regexes:
                expr_str = re.sub(pattern, repl_func, expr_str)
            xml_struct.attrib[attrib] = expr_str
        for xml_child in xml_struct:
            self.replace_tokens(xml_child)

    @staticmethod
    def copy_dict_info(own_dict: dict, other_dict: dict) -> None:
        """Add information from other dict if we didn't have it yet"""
        for key in other_dict.keys():
            if key not in own_dict:
                own_dict[key] = other_dict[key]

    def copy_xml_dicts(self, other_parser: 'XmlParser') -> None:
        """Copy information necessary for linking and generation from another parser as if we'd read the file"""
        if self.versions and other_parser.versions:
            [self.versions.versions.append(version) for version in other_parser.versions.versions]
        self.tokens.extend(other_parser.tokens)
        self.copy_dict_info(self.verattrs, other_parser.verattrs)
        self.copy_dict_info(self.path_dict, other_parser.path_dict)
        self.copy_dict_info(self.tag_dict, other_parser.tag_dict)
        if self.basics and other_parser.basics:
            self.basics.add_other_basics(other_parser.basics)
        self.copy_dict_info(self.processed_types, other_parser.processed_types)
        self.generic_types.update(other_parser.generic_types)
        self.numpy_types.update(other_parser.numpy_types)

    @staticmethod
    def get_attr_with_backups(field: 'Element', attribute_keys: list[str]) -> str | None:
        """Return the value of the first attribute in the list that exists and is not None."""
        return next((value for key in attribute_keys if (value := field.attrib.get(key))), None)

    @staticmethod
    def get_attr_with_array_alt(field: 'Element', attribute_name: str) -> str | list[str] | None:
        """
        Return either a string of the matching attribute or a list of all
        continuous <attribute><nr> attributes, starting from 1.
        """
        value = field.attrib.get(attribute_name)
        if value is not None:
            return value

        # Use itertools to generate names 'attr1', 'attr2', ... and take them
        # as long as they exist in the dictionary.
        array_keys = (f"{attribute_name}{i}" for i in itertools.count(1))
        array_value = list(itertools.takewhile(
            lambda key: key in field.attrib,
            array_keys
        ))

        # Map the found keys back to their values
        if array_value:
            return [field.attrib[key] for key in array_value]

        return None

    def interpret_boolean(self, f_type: str, default_string: str) -> str | None:
        if self.basics and f_type in self.path_dict and self.tag_dict[f_type.lower()] == "basic" and f_type in self.basics.booleans:
            # boolean basics *can* be used as booleans, but don't have to be
            if default_string.capitalize() in ("True", "False"):
                default_string = default_string.capitalize()
                return default_string
        return None

    def get_class_path_segments(self, child: 'Element') -> list[str]:
        """
        Determines the folder and file segments for a class-like XML element.
        """
        class_name = child.attrib["name"]
        if child.tag == "module":
            return [class_name]
        if child.tag == "basic":
            return ["basic"]
        # Force any struct_type to structs folder
        folder_name = "structs" if child.tag in self.struct_types else pluralize_name(child.tag)
        return [folder_name, class_name]
