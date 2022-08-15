import importlib
import logging
import xml.etree.ElementTree as ET
import os
import distutils.dir_util as dir_util
from html import unescape
import traceback
from numpy import ndarray

from codegen import naming_conventions as convention
from codegen.BaseClass import BaseClass
from codegen.Basics import Basics
from codegen.Compound import Compound
from codegen.Enum import Enum
from codegen.Bitfield import Bitfield
from codegen.Versions import Versions
from codegen.Module import Module
from codegen.naming_conventions import clean_comment_str

logging.basicConfig(level=logging.DEBUG)


class XmlParser:
    struct_types = ("compound", "niobject", "struct")
    bitstruct_types = ("bitfield", "bitflags", "bitstruct")
    builtin_literals = {'str': '', 'float': 0.0, 'int': 0, 'bool': False}

    def __init__(self, format_name):
        """Set up the xml parser."""

        self.format_name = format_name
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
            "basic_map": os.path.join(self.base_segments, "basic"),
            "versions": self.base_segments,
            "ContextReference": "context",
            "BaseEnum": "base_enum",
            "BaseStruct": "base_struct",
            }
        # enum name -> storage name
        self.storage_dict = {}
        # maps each type to its member tag type
        self.tag_dict = {}

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
                name_safe_tag = child.tag
                if child.tag == "module":
                    # for modules, set the path to base/module_name
                    class_name = child.attrib["name"]
                    class_segments = [class_name]
                elif child.tag == "basic":
                    class_segments = ["basic"]
                    class_name = child.attrib["name"]
                    if Basics.suitable_for_enum(child):
                        self.path_dict[Enum.base_from_storage(class_name)] = os.path.join(base_segments, 'enums',)
                        # self.path_dict[Enum.base_from_storage(class_name)] = os.path.join(base_segments, 'enum',)
                else:
                    name_safe_tag = child.tag + "s"
                    # for classes, set the path to module_path/tag/class_name or
                    # base/tag/class_name if it's not part of a module
                    class_name = child.attrib["name"]
                    if child.attrib.get("module"):
                        base_segments = self.path_dict[child.attrib["module"]]
                    # if child.tag == "enum":
                    #     tag = "enums"
                    class_segments = [name_safe_tag, class_name, ]
                # store the final relative module path for this class
                self.path_dict[class_name] = os.path.join(base_segments, *class_segments)
                # self.tag_dict[class_name.lower()] = child.tag
                self.tag_dict[class_name.lower()] = name_safe_tag

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

        self.versions = Versions(self)
        self.basics = Basics(self, BaseClass.get_out_path(self.path_dict["basic_map"]))

        self.generate_module_paths(root, xml_path, parsed_xmls)

        for child in root:
            try:
                if child.tag in self.struct_types:
                    Compound(self, child)
                elif child.tag in self.bitstruct_types:
                    Bitfield(self, child)
                elif child.tag == "basic":
                    self.basics.read(child)
                elif child.tag == "enum":
                    Enum(self, child)
                elif child.tag == "module":
                    Module(self, child)
                elif child.tag == "version":
                    self.versions.read(child)
                elif child.tag == "verattr":
                    self.read_verattr(child)
            except Exception as err:
                logging.error(err)
                traceback.print_exc()
        out_file = BaseClass.get_out_path(os.path.join(self.base_segments, "versions"))
        self.versions.write(out_file)
        # self.basics.write_basic_map()
        parsed_xmls[xml_path] = self

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
            new_parser = XmlParser(format_name)
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
        if struct.tag in ("version", "token"):
            # don't apply conventions to these types (or there are none to apply)
            return
        elif struct.tag == "verattr":
            self.apply_convention(struct, convention.name_class, ("type",))
            self.apply_convention(struct, convention.name_access, ("access",))
        elif struct.tag == "module":
            self.apply_convention(struct, convention.name_module, ("name", "depends"))
            self.apply_convention(struct, convention.force_bool, ("custom",))
            struct.text = clean_comment_str(struct.text, indent="", class_comment='"""')[2:]
        else:
            # it is a tag with a class
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
                for field in struct:
                    self.apply_convention(field, convention.name_attribute, ("name",))
                    self.apply_convention(field, convention.name_class, ("type",))
            elif struct.tag in self.struct_types:
                self.apply_convention(struct, convention.force_bool, ("generic",))
                # a struct's fields
                for field in struct:
                    self.apply_convention(field, convention.name_attribute, ("name",))
                    self.apply_convention(field, convention.name_class, ("type", "onlyT", "excludeT"))
                    # template can refer to a type of an attribute
                    self.apply_convention(field, convention.format_potential_tuple, ("default",))
                    for default in field:
                        self.apply_convention(field, convention.name_class, ("onlyT",))
                        self.apply_convention(field, convention.format_potential_tuple, ("value",))
            # filter comment str
            struct.text = clean_comment_str(struct.text, indent="\t", class_comment='"""')

    @staticmethod
    def arrs_to_tuple(*args):
        valid_arrs = tuple(str(arr) for arr in args if arr)
        arr_str = f'({", ".join(valid_arrs)},)'
        return arr_str

    def read_for_type(self, dtype, context, arg=0, template=None, arr1=None, arr2=None):
        if arr1 is not None:
            return f'Array.from_stream(stream, {context}, {arg}, {template}, {self.arrs_to_tuple(arr1, arr2)}, {dtype})'
        else:
            # use the standard functionality
            return f'{dtype}.from_stream(stream, {context}, {arg}, {template})'

    def write_for_type(self, dtype, attr, context, arg=0, template=None, arr1=None, arr2=None):
        if arr1:
            return f'Array.to_stream(stream, {attr}, {self.arrs_to_tuple(arr1, arr2)}, '\
                   f'{dtype}, {context}, {arg}, {template})'
        else:
            # use the standard functionality
            return f'{dtype}.to_stream(stream, {attr})'

    def map_type(self, in_type, array=False):
        has_stream_functions = False
        if array:
            out_type = ('Array', in_type)
        else:
            out_type = in_type
        if in_type in self.path_dict:
            l_type = in_type.lower()
            if self.tag_dict.get(l_type) == "basic":
                basic_class = self.basics.basic_map[in_type]
                if callable(getattr(basic_class, "functions_for_stream", None)):
                    has_stream_functions = True
                    if array:
                        if callable(getattr(basic_class, "create_array", None)):
                            test = basic_class.create_array(1)
                            if isinstance(test, ndarray):
                                out_type = ('numpy', f'numpy.{repr(test.dtype)}')
                    else:
                        if callable(getattr(basic_class, "from_value", None)):
                            # check from_value to see which builtin it returns
                            test = basic_class.from_value(0)
                            test_type = type(test).__name__
                            if test_type in self.builtin_literals:
                                out_type = test_type
        return has_stream_functions, out_type

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
        fixed_tokens = (("\\", "."), ("#ARG#", "arg"), ("#T#", "template"))
        for attrib, expr_str in xml_struct.attrib.items():
            for op_token, op_str in fixed_tokens:
                expr_str = expr_str.replace(op_token, op_str)
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
        [self.versions.read(version) for version in other_parser.versions.versions]
        self.tokens.extend(other_parser.tokens)
        self.copy_dict_info(self.verattrs, other_parser.verattrs)
        self.copy_dict_info(self.path_dict, other_parser.path_dict)
        self.copy_dict_info(self.storage_dict, other_parser.storage_dict)
        self.copy_dict_info(self.tag_dict, other_parser.tag_dict)
        self.basics.add_other_basics(other_parser.basics, other_parser.path_dict["basic_map"])


def copy_src_to_generated(src_dir, trg_dir):
    """copies the files from the source folder to the generated folder"""
    # remove old codegen
    dir_util.remove_tree(trg_dir)
    # necessary to not error if you have manually removed a subdirectory in generated
    dir_util._path_created = {}
    # do the actual copying
    dir_util.copy_tree(src_dir, trg_dir)


def create_inits(base_dir):
    """Create a __init__.py file in all subdirectories that don't have one, to prevent error on second import"""
    init_file = "__init__.py"
    for root, dirs, files in os.walk(base_dir):
        if init_file not in files:
            # __init__.py does not exist, create it
            with open(os.path.join(root, init_file), 'x'):
                pass
        # don't go into subdirectories that start with a double underscore
        dirs[:] = [dirname for dirname in dirs if dirname[:2] != '__']


def stash_inits(target_dir):
    """Move all __init__.py files over to a temporary directory to prevent execution when loading submodules
    and replace them with empty init files"""
    init_file = "__init__.py"
    i = 0
    temp_base = os.path.join(os.getcwd(), ".temp")
    temp_dir = f'{temp_base}{i}'
    no_overwrite = False
    if no_overwrite:
        while os.path.exists(temp_dir):
            i += 1
            temp_dir = f'{temp_base}{i}'
    else:
        if os.path.exists(temp_dir):
            dir_util.remove_tree(temp_dir)
    os.makedirs(temp_dir)
    for dirpath, dirnames, filenames in os.walk(target_dir):
        if init_file in filenames:
            rel_path = os.path.relpath(dirpath, target_dir)
            os.renames(os.path.join(dirpath, init_file), os.path.join(temp_dir, rel_path, init_file))
    create_inits(target_dir)
    return temp_dir


def apply_stash(stashed_dir, target_dir):
    """Move the files in a stashed directory to the target directory, removing the temporary directory"""
    dir_util.copy_tree(stashed_dir, target_dir)
    dir_util.remove_tree(stashed_dir)


def apply_autopep8(target_dir):
    """Run autopep8 --in-place on the target directory, if that package is installed"""
    if importlib.util.find_spec("autopep8"):
        import autopep8
        options = autopep8.parse_args(arguments=['-i', '-r', target_dir])
        autopep8.fix_multiple_files([target_dir], options=options)
    else:
        logging.warn("Tried to run autopep8, but module not found.")


def generate_classes():
    logging.info("Starting class generation")
    cwd = os.getcwd()
    source_dir = os.path.join(cwd, "source")
    target_dir = os.path.join(cwd, "generated")
    root_dir = os.path.join(source_dir, "formats")
    copy_src_to_generated(source_dir, target_dir)
    stashed_dir = stash_inits(target_dir)
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
                    xmlp = XmlParser(format_name)
                    xmlp.load_xml(xml_path, parsed_xmls)
    apply_stash(stashed_dir, target_dir)
    create_inits(target_dir)


generate_classes()
