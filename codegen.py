import importlib
import logging
import re
import xml.etree.ElementTree as ET
import os
import shutil
import fnmatch
import argparse
import traceback

from html import unescape

from codegen import naming_conventions as convention
from codegen.BaseClass import BaseClass
from codegen.Basics import Basics
from codegen.Compound import Compound
from codegen.Enum import Enum
from codegen.Bitfield import Bitfield
from codegen.Imports import Imports
from codegen.Versions import Versions
from codegen.Module import Module
from codegen.naming_conventions import clean_comment_str

logging.basicConfig(level=logging.DEBUG)

arg_regex = re.compile(r"(#ARG)([0-9]*)(#)")
template_regex = re.compile(r"(#T)([0-9]*)(#)")


class XmlParser:
    struct_types = ("compound", "niobject", "struct")
    bitstruct_types = ("bitfield", "bitflags", "bitstruct")
    builtin_literals = {'str': '', 'float': 0.0, 'int': 0, 'bool': False}

    def __init__(self, format_name, gen_dir="generated"):
        """Set up the xml parser."""

        self.format_name = format_name
        self.gen_dir = gen_dir
        self.base_segments = os.path.join("formats", self.format_name)
        # which encoding to use for the output files
        self.encoding = 'utf-8'

        # elements for versions
        self.versions = None

        # ordered (!) list of tuples ({tokens}, (target_attribs)) for each <token>
        self.tokens = []

        # maps version attribute name to [access, type]
        self.verattrs = {}
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
        # maps each type to its member tag type
        self.tag_dict = {}
        # order is relevant to ensure that structs are later imported in the correct order in generated code
        self.processed_types = {}

        self.basics = None

    def generate_module_paths(self, root, xml_path, parsed_xmls):
        """preprocessing - generate module paths for imports relative to the output dir"""
        for child in root:
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
                base_segments = self.base_segments
                if child.tag == "module":
                    # for modules, set the path to base/module_name
                    class_name = child.attrib["name"]
                    class_segments = [class_name]
                elif child.tag == "basic":
                    class_name = child.attrib["name"]
                    class_segments = ["basic"]
                else:
                    # for classes, set the path to module_path/tag/class_name or
                    # base/tag/class_name if it's not part of a module
                    class_name = child.attrib["name"]
                    if child.attrib.get("module"):
                        base_segments = self.path_dict[child.attrib["module"]]
                    class_segments = [f"{child.tag}s", class_name, ]
                # store the final relative module path for this class
                self.path_dict[class_name] = os.path.join(base_segments, *class_segments)
                self.tag_dict[class_name.lower()] = child.tag

    def load_xml(self, xml_file, parsed_xmls=None):
        """Loads an XML (can be filepath or open file) and does all parsing
        Goes over all children of the root node and calls the appropriate function depending on type of the child"""
        try:
            # try for case where xml_file is a passed file object
            xml_path = xml_file.name
        except AttributeError:
            # if attribute error, assume it was a file path
            xml_path = xml_file
        xml_path = os.path.realpath(xml_path)
        # dictionary of xml file: XmlParser
        if parsed_xmls is None:
            parsed_xmls = {}

        tree = ET.parse(xml_file)
        root = tree.getroot()

        self.versions = Versions(self, gen_dir=self.gen_dir)
        self.basics = Basics(self)

        self.generate_module_paths(root, xml_path, parsed_xmls)

        for child in root:
            try:
                if child.tag in self.struct_types:
                    Compound(self, child, gen_dir=self.gen_dir)
                elif child.tag in self.bitstruct_types:
                    Bitfield(self, child, gen_dir=self.gen_dir)
                elif child.tag == "basic":
                    self.basics.read(child)
                elif child.tag == "enum":
                    Enum(self, child, gen_dir=self.gen_dir)
                elif child.tag == "module":
                    Module(self, child, gen_dir=self.gen_dir)
                elif child.tag == "version":
                    self.versions.read(child)
                elif child.tag == "verattr":
                    self.read_verattr(child)
            except:
                logging.exception(f"Parsing child {child} failed")
        versions_file = BaseClass.get_out_path(os.path.join(self.base_segments, "versions"), gen_dir=self.gen_dir)
        self.versions.write(versions_file)
        imports_module = os.path.join(self.base_segments, "imports")
        self.write_import_map(BaseClass.get_out_path(imports_module, gen_dir=self.gen_dir))
        init_file_path = BaseClass.get_out_path(os.path.join(self.base_segments, "__init__"), gen_dir=self.gen_dir)
        import_string = f'from {Imports.import_from_module_path(imports_module, gen_dir=self.gen_dir)} import name_type_map\n'
        if not os.path.exists(init_file_path):
            with open(init_file_path, "w", encoding=self.encoding) as f:
                f.write(import_string)
        else:
            with open(init_file_path, "r+", encoding=self.encoding) as f:
                init_content = f.read()
                f.seek(0, 0)
                f.write(import_string)
                f.write(init_content)

        parsed_xmls[xml_path] = self

    def write_import_map(self, file):
        with open(file, "w", encoding=self.encoding) as f:
            f.write("from importlib import import_module\n")
            f.write("\n\ntype_module_name_map = {\n")
            for type_name in self.processed_types:
                f.write(f"\t'{type_name}': '{Imports.import_from_module_path(self.path_dict[type_name], gen_dir=self.gen_dir)}',\n")
            f.write('}\n')
            f.write("\nname_type_map = {}\n")
            f.write("for type_name, module in type_module_name_map.items():\n")
            f.write("\tname_type_map[type_name] = getattr(import_module(module), type_name)\n")
            f.write("for class_object in name_type_map.values():\n")
            f.write("\tif callable(getattr(class_object, 'init_attributes', None)):\n")
            f.write("\t\tclass_object.init_attributes()\n")

    # the following constructs do not create classes
    def read_token(self, token):
        """Reads an xml <token> block and stores it in the tokens list"""
        self.tokens.append(([(sub_token.attrib["token"], sub_token.attrib["string"])
                            for sub_token in token],
                            token.attrib["attrs"].split(" ")))

    def read_verattr(self, verattr):
        """Reads an xml <verattr> and stores it in the verattrs dict"""
        name = verattr.attrib['name']
        assert name not in self.verattrs, f"verattr {name} already defined!"
        access = verattr.attrib['access']
        attr_type = verattr.attrib.get('type')
        self.verattrs[name] = [access, attr_type]

    def read_xinclude(self, xinclude, xml_path, parsed_xmls):
        """Reads an xi:include element, and parses the linked xml if it doesn't exist yet in parsed xmls"""
        # convert the linked relative path to an absolute one
        new_path = os.path.realpath(os.path.join(os.path.dirname(xml_path), xinclude.attrib['href']))
        # check if the xml file was already parsed
        if new_path not in parsed_xmls:
            # if not, parse it now
            format_name = os.path.splitext(os.path.basename(new_path))[0]
            new_parser = XmlParser(format_name, gen_dir=self.gen_dir)
            new_parser.load_xml(new_path, parsed_xmls)
        else:
            new_parser = parsed_xmls[new_path]
        # append all pertinent information (file paths etc) to self for access
        self.copy_xml_dicts(new_parser)

    @staticmethod
    def apply_convention(struct, func, params):
        for k in params:
            if struct.attrib.get(k):
                struct.attrib[k] = func(struct.attrib[k])

    def apply_conventions(self, struct):
        # struct top level
        if struct.tag in ("token",):
            # don't apply conventions to these types (or there are none to apply)
            return
        elif struct.tag == "version":
            self.apply_convention(struct, convention.force_bool, ("supported", "custom"))
        elif struct.tag == "verattr":
            self.apply_convention(struct, convention.name_class, ("type",))
            self.apply_convention(struct, convention.name_access, ("access",))
        elif struct.tag == "module":
            self.apply_convention(struct, convention.name_module, ("name", "depends"))
            self.apply_convention(struct, convention.force_bool, ("custom",))
            struct.text = clean_comment_str(struct.text, indent="", class_comment='"""')[2:]
        else:
            # it is a tag with a class
            struct.attrib["__name__"] = struct.attrib["name"]
            self.apply_convention(struct, convention.name_class, ("name", "inherit"))
            self.apply_convention(struct, convention.name_module, ("module",))
            if struct.tag == "basic":
                self.apply_convention(struct, convention.force_bool, ("boolean", "integral", "countable", "generic"))
            elif struct.tag == "enum":
                self.apply_convention(struct, convention.name_class, ("storage",))
                for option in struct:
                    self.apply_convention(option, convention.name_enum_key_if_necessary, ("name", ))
            elif struct.tag in self.bitstruct_types:
                self.apply_convention(struct, convention.name_class, ("storage",))
                # a bitfield/bitflags fields
                if struct.tag == 'bitflags':
                    for field in struct:
                        field.attrib['enum_name'] = convention.name_enum_key_if_necessary(field.attrib['name'])
                for field in struct:
                    self.apply_convention(field, convention.name_attribute, ("name",))
                    self.apply_convention(field, convention.name_class, ("type",))
            elif struct.tag in self.struct_types:
                self.apply_convention(struct, convention.force_bool, ("generic",))
                # a struct's fields
                for field in struct:
                    self.apply_convention(field, convention.name_attribute, ("name",))
                    self.apply_convention(field, convention.name_class, ("type", "onlyT", "excludeT"))
                    self.apply_convention(field, convention.force_bool, ("optional", "abstract", "recursive"))
                    # template can refer to a type of an attribute
                    self.apply_convention(field, convention.format_potential_tuple, ("default",))
                    for default in field:
                        self.apply_convention(default, convention.name_class, ("onlyT",))
                        self.apply_convention(default, convention.format_potential_tuple, ("value",))
            # filter comment str
            struct.text = clean_comment_str(struct.text, indent="\t", class_comment='"""')

    @staticmethod
    def match_replace_function(base_string):
        def match_replace(match_object):
            if match_object.group(2):
                indexing = f'_{match_object.group(2)}'
            else:
                indexing = ''
            return f'{base_string}{indexing}'
        return match_replace

    def replace_tokens(self, xml_struct):
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
        # additional tokens that are not specified by nif.xml
        fixed_tokens = (("\\", "."), ("#SELF#", "instance"))
        fixed_array_parts = ((arg_regex, "arg"), (template_regex, "template"))
        for attrib, expr_str in xml_struct.attrib.items():
            for op_token, op_str in fixed_tokens:
                expr_str = expr_str.replace(op_token, op_str)
            for part_regex, base_string in fixed_array_parts:
                expr_str = re.sub(part_regex, self.match_replace_function(base_string), expr_str)
            xml_struct.attrib[attrib] = expr_str
        for xml_child in xml_struct:
            self.replace_tokens(xml_child)

    @staticmethod
    def copy_dict_info(own_dict, other_dict):
        """Add information from other dict if we didn't have it yet"""
        for key in other_dict.keys():
            if key not in own_dict:
                own_dict[key] = other_dict[key]

    def copy_xml_dicts(self, other_parser):
        """Copy information necessary for linking and generation from another parser as if we'd read the file"""
        [self.versions.versions.append(version) for version in other_parser.versions.versions]
        self.tokens.extend(other_parser.tokens)
        self.copy_dict_info(self.verattrs, other_parser.verattrs)
        self.copy_dict_info(self.path_dict, other_parser.path_dict)
        self.copy_dict_info(self.tag_dict, other_parser.tag_dict)
        self.basics.add_other_basics(other_parser.basics)
        self.copy_dict_info(self.processed_types, other_parser.processed_types)

    @staticmethod
    def get_attr_with_backups(field, attribute_keys):
        # return the value of the first attribute in the list that is not empty or missing
        for key in attribute_keys:
            attr_value = field.attrib.get(key)
            if attr_value:
                return attr_value
        else:
            return None

    @staticmethod
    def get_attr_with_array_alt(field, attribute_name):
        # return either a string of the matching attribute, or a list of all continuous <attribute><nr> attributes,
        # starting from 1
        value = field.attrib.get(attribute_name, None)
        if value is None:
            array_value = []
            i = 1
            current_entry = field.attrib.get(f"{attribute_name}{i}", None)
            while current_entry is not None:
                array_value.append(current_entry)
                i += 1
                current_entry = field.attrib.get(f"{attribute_name}{i}", None)

            if array_value:
                value = array_value

        return value

    def interpret_boolean(self, f_type, default_string):
        if f_type in self.path_dict and self.tag_dict[f_type.lower()] == "basic" and f_type in self.basics.booleans:
            # boolean basics *can* be used as booleans, but don't have to be
            if default_string.capitalize() in ("True", "False"):
                default_string = default_string.capitalize()
                return default_string
        return None


def copy_src_to_generated(src_dir, trg_dir):
    """copies the files from the source folder to the generated folder"""
    # remove old codegen
    if os.path.exists(trg_dir):
        shutil.rmtree(trg_dir)
    # do the actual copying (ignore .git folders because there's trouble deleting them)
    shutil.copytree(src_dir, trg_dir, ignore=shutil.ignore_patterns('.git',))


def fix_imports(gen_dir):
    """Fixes hardcoded imports in non-generated files"""
    basename = os.path.basename(gen_dir)
    for path, _, files in os.walk(os.path.abspath(gen_dir)):
        for filename in fnmatch.filter(files, "*.py"):
            filepath = os.path.join(path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                s = f.read()
            s = s.replace("from generated.", f"from {basename}.")
            s = s.replace("import generated.", f"import {basename}.")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(s)


def create_inits(base_dir):
    """Create a __init__.py file in all subdirectories that don't have one, to prevent error on second import"""
    init_name = "__init__.py"
    for root, dirs, files in os.walk(base_dir):
        if init_name not in files:
            # __init__.py does not exist, create it
            with open(os.path.join(root, init_name), 'x'):
                pass
        # don't go into subdirectories that start with a double underscore
        dirs[:] = [dirname for dirname in dirs if dirname[:2] != '__']


def apply_autopep8(target_dir):
    """Run autopep8 --in-place on the target directory, if that package is installed"""
    if importlib.util.find_spec("autopep8"):
        import autopep8
        options = autopep8.parse_args(arguments=['-i', '-r', target_dir])
        autopep8.fix_multiple_files([target_dir], options=options)
    else:
        logging.warn("Tried to run autopep8, but module not found.")


def generate_classes(gen_dir, silent):
    try:
        if silent:
            logging.disable(logging.ERROR)
        logging.info("Starting class generation")
        cwd = os.getcwd()
        source_dir = os.path.join(cwd, "source")
        target_dir = os.path.join(cwd, gen_dir)
        root_dir = os.path.join(source_dir, "formats")
        copy_src_to_generated(source_dir, target_dir)
        fix_imports(target_dir)
        parsed_xmls = {}
        for format_name in os.listdir(root_dir):
            dir_path = os.path.join(root_dir, format_name)
            if os.path.isdir(dir_path):
                xml_path = os.path.join(dir_path, format_name+".xml")
                if os.path.isfile(xml_path):
                    if os.path.realpath(xml_path) in parsed_xmls:
                        logging.info(f"Already read {format_name}, skipping")
                    else:
                        logging.info(f"Reading {format_name} format")
                        xmlp = XmlParser(format_name, gen_dir=gen_dir)
                        xmlp.load_xml(xml_path, parsed_xmls)
        create_inits(target_dir)
        if silent:
            logging.disable(logging.NOTSET)
        return 0
    except:
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='codegen')
    parser.add_argument('-g', '--generated-dir', default="generated")
    parser.add_argument('--silent', action='store_true')
    args = parser.parse_args()
    exit_code = generate_classes(gen_dir=args.generated_dir, silent=args.silent)
    try:
        exit(exit_code)
    except NameError:
        pass
