import logging
import xml.etree.ElementTree as ET
import os
from distutils.dir_util import copy_tree
from html import unescape
import traceback

from codegen import naming_conventions as convention
from codegen.Compound import Compound
from codegen.Enum import Enum
from codegen.Bitfield import Bitfield
from codegen.Versions import Versions
from codegen.Module import Module
from codegen.naming_conventions import clean_comment_str

logging.basicConfig(level=logging.DEBUG)

FIELD_TYPES = ("add", "field")
VER = "self.context.version"


class XmlParser:
    struct_types = ("compound", "niobject", "struct")
    bitstruct_types = ("bitfield", "bitflags", "bitstruct")

    def __init__(self, format_name):
        """Set up the xml parser."""

        self.format_name = format_name
        # which encoding to use for the output files
        self.encoding='utf-8'

        # elements for versions
        self.version_string = None

        # ordered (!) list of tuples ({tokens}, (target_attribs)) for each <token>
        self.tokens = []
        self.versions = [([], ("versions", "until", "since")), ]

        # maps each type to its generated py file's relative path
        self.path_dict = {}
        # enum name -> storage name
        self.storage_dict = {}
        # maps each type to its member tag type
        self.tag_dict = {}

    def generate_module_paths(self, root):
        """preprocessing - generate module paths for imports relative to the output dir"""
        for child in root:
            # only check stuff that has a name - ignore version tags
            if child.tag not in ("version", "token"):
                base_segments = os.path.join("formats", self.format_name)
                if child.tag == "module":
                    # for modules, set the path to base/module_name
                    class_name = convention.name_module(child.attrib["name"])
                    class_segments = [class_name]
                else:
                    # for classes, set the path to module_path/tag/class_name or
                    # base/tag/class_name if it's not part of a module
                    class_name = convention.name_class(child.attrib["name"])
                    if child.attrib.get("module"):
                        base_segments = self.path_dict[convention.name_module(child.attrib["module"])]
                    class_segments = [child.tag, class_name, ]
                # store the final relative module path for this class
                self.path_dict[class_name] = os.path.join(base_segments, *class_segments)
                self.tag_dict[class_name.lower()] = child.tag

        self.path_dict["Array"] = "array"
        self.path_dict["BasicBitfield"] = "bitfield"
        self.path_dict["BitfieldMember"] = "bitfield"
        self.path_dict["ContextReference"] = "context"
        self.path_dict["UbyteEnum"] = "base_enum"
        self.path_dict["UshortEnum"] = "base_enum"
        self.path_dict["UintEnum"] = "base_enum"
        self.path_dict["Uint64Enum"] = "base_enum"

    def load_xml(self, xml_file):
        """Loads an XML (can be filepath or open file) and does all parsing
        Goes over all children of the root node and calls the appropriate function depending on type of the child"""
        tree = ET.parse(xml_file)
        root = tree.getroot()
        self.generate_module_paths(root)
        versions = Versions(self)

        for child in root:
            self.replace_tokens(child)
            if child.tag not in ('version', 'module'):
                self.apply_conventions(child)
            try:
                if child.tag in self.struct_types:
                    Compound(self, child)
                elif child.tag in self.bitstruct_types:
                    Bitfield(self, child)
                # elif child.tag == "basic":
                #     self.write_basic(child)
                elif child.tag == "enum":
                    Enum(self, child)
                elif child.tag == "module":
                    Module(self, child)
                elif child.tag == "version":
                    versions.read(child)
                elif child.tag == "token":
                    self.read_token(child)
            except Exception as err:
                logging.error(err)
                traceback.print_exc()
        out_file = os.path.join(os.getcwd(), "generated", "formats", self.format_name, "versions.py")
        versions.write(out_file)

    # the following constructs do not create classes
    def read_token(self, token):
        """Reads an xml <token> block and stores it in the tokens list"""
        self.tokens.append(([(sub_token.attrib["token"], sub_token.attrib["string"])
                            for sub_token in token],
                            token.attrib["attrs"].split(" ")))

    @staticmethod
    def apply_convention(struct, func, params):
        for k in params:
            if struct.attrib.get(k):
                struct.attrib[k] = func(struct.attrib[k])

    def apply_conventions(self, struct):
        # struct top level
        self.apply_convention(struct, convention.name_class, ("name", "inherit"))
        # a struct's fields
        for field in struct:
            if field.tag in FIELD_TYPES:
                self.apply_convention(field, convention.name_attribute, ("name",))
                self.apply_convention(field, convention.name_class, ("type",))
                self.apply_convention(field, convention.name_class, ("onlyT",))
                self.apply_convention(field, convention.name_class, ("excludeT",))
                for default in field:
                    self.apply_convention(field, convention.name_class, ("onlyT",))

        # filter comment str
        struct.text = clean_comment_str(struct.text, indent="\t", class_comment='"""')

    def method_for_type(self, dtype: str, mode="read", attr="self.dummy", arg=None, template=None):
        if self.tag_dict[dtype.lower()] == "enum":
            storage = self.storage_dict[dtype]
            io_func = f"{mode}_{storage.lower()}"
            if mode == "read":
                return f"{attr} = {dtype}(stream.{io_func}())"
            elif mode == "write":
                return f"stream.{io_func}({attr}.value)"

        args = ""
        if arg:
            args = f", ({arg}, {template})"
        # template or custom type
        if "template" in dtype.lower() or self.tag_dict[dtype.lower()] != "basic":
            io_func = f"{mode}_type"
            if self.tag_dict[dtype.lower()] != "bitfield":
                args = f", (self.context, {arg}, {template})"
        # basic type
        else:
            io_func = f"{mode}_{dtype.lower()}"
            dtype = ""
        if mode == "read":
            return f"{attr} = stream.{io_func}({dtype}{args})"
        elif mode == "write":
            return f"stream.{io_func}({attr})"

    def map_type(self, in_type):
        l_type = in_type.lower()
        if self.tag_dict.get(l_type) != "basic":
            return True, in_type
        else:
            if "float" in l_type:
                return False, "float"
            elif l_type == "bool":
                return False, "bool"
            else:
                return False, "int"
            
    def replace_tokens(self, xml_struct):
        """Update xml_struct's (and all of its children's) attrib dict with content of tokens+versions list."""
        # replace versions after tokens because tokens include versions
        for tokens, target_attribs in self.tokens + self.versions:
            for target_attrib in target_attribs:
                if target_attrib in xml_struct.attrib:
                    expr_str = xml_struct.attrib[target_attrib]
                    for op_token, op_str in tokens:
                        expr_str = expr_str.replace(op_token, op_str)
                    # get rid of any remaining html escape characters
                    xml_struct.attrib[target_attrib] = unescape(expr_str)
        # additional tokens that are not specified by nif.xml
        # ("User Version", "user_version"), ("BS Header\\BS Version", "bs_header\\bs_version"), ("Version", "version")
        fixed_tokens = (("\\", "."), ("#ARG#", "arg"), ("#T#", "self.template"))
        for attrib, expr_str in xml_struct.attrib.items():
            for op_token, op_str in fixed_tokens:
                expr_str = expr_str.replace(op_token, op_str)
            xml_struct.attrib[attrib] = expr_str
        for xml_child in xml_struct:
            self.replace_tokens(xml_child)


def copy_src_to_generated():
    """copies the files from the source folder to the generated folder"""
    cwd = os.getcwd()
    src_dir = os.path.join(cwd, "source")
    trg_dir = os.path.join(cwd, "generated")
    copy_tree(src_dir, trg_dir)


def create_inits():
    """Create a __init__.py file in all subdirectories that don't have one, to prevent error on second import"""
    base_dir = os.path.join(os.getcwd(), 'generated')
    init_file = "__init__.py"
    for root, dirs, files in os.walk(base_dir):
        if init_file not in files:
            # __init__.py does not exist, create it
            with open(os.path.join(root, init_file), 'x'): pass
        # don't go into subdirectories that start with a double underscore
        dirs[:] = [dirname for dirname in dirs if dirname[:2] != '__']

def generate_classes():
    logging.info("Starting class generation")
    cwd = os.getcwd()
    root_dir = os.path.join(cwd, "source\\formats")
    copy_src_to_generated()
    for format_name in os.listdir(root_dir):
        dir_path = os.path.join(root_dir, format_name)
        if os.path.isdir(dir_path):
            xml_path = os.path.join(dir_path, format_name+".xml")
            if os.path.isfile(xml_path):
                logging.info(f"Reading {format_name} format")
                xmlp = XmlParser(format_name)
                xmlp.load_xml(xml_path)
    create_inits()


generate_classes()
