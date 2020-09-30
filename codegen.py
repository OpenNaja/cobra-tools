import logging
import xml.etree.ElementTree as ET
import os
from distutils.dir_util import copy_tree
from xml.etree import ElementTree
from html import unescape
import traceback

from codegen import naming_conventions as convention
from codegen.expression import Expression
from codegen.Compound import Compound
from codegen.Enum import Enum
from codegen.Bitfield import Bitfield
from codegen.naming_conventions import clean_comment_str

logging.basicConfig(level=logging.DEBUG)

FIELD_TYPES = ("add", "field")
VER = "stream.version"


def write_file(filename: str, contents: str):
    file_dir = os.path.dirname(filename)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(contents)


class XmlParser:
    struct_types = ("compound", "niobject", "struct")
    bitstruct_types = ("bitfield", "bitflags", "bitstruct")

    def __init__(self, format_name):
        """Set up the xml parser."""

        self.format_name = format_name
        # initialize dictionaries
        # map each supported version string to a version number
        versions = {}
        # map each supported game to a list of header version numbers
        games = {}
        # note: block versions are stored in the _games attribute of the struct class

        # elements for creating new classes
        self.class_name = None
        self.class_dict = None
        self.base_class = ()
        #
        # self.basic_classes = []
        # # these have to be read as basic classes
        # self.compound_classes = []

        # elements for versions
        self.version_string = None

        # ordered (!) list of tuples ({tokens}, (target_attribs)) for each <token>
        self.tokens = []
        self.versions = [ ([], ("versions", "until", "since")), ]

        # maps each type to its generated py file's relative path
        self.path_dict = {}
        # maps each type to its member tag type
        self.tag_dict = {}

        self.storage_types = set()

    def generate_module_paths(self, root):
        """preprocessing - generate module paths for imports relative to the output dir"""
        for child in root:
            # only check stuff that has a name - ignore version tags
            if child.tag not in ("version", "module", "token"):
                class_name = convention.name_class(child.attrib["name"])
                out_segments = ["formats", self.format_name, child.tag, ]
                if child.tag == "niobject":
                    out_segments.append(child.attrib["module"])
                out_segments.append(class_name)
                # store the final relative module path for this class
                self.path_dict[class_name] = os.path.join(*out_segments)
                self.tag_dict[class_name.lower()] = child.tag

        self.path_dict["BasicBitfield"] = "bitfield"
        self.path_dict["BitfieldMember"] = "bitfield"

    def load_xml(self, xml_file):
        """Loads an XML (can be filepath or open file) and does all parsing
        Goes over all children of the root node and calls the appropriate function depending on type of the child"""
        # try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        self.generate_module_paths(root)

        for child in root:
            self.replace_tokens(child)
            self.apply_conventions(child)
            try:
                if child.tag in self.struct_types:
                    Compound(self, child)
                # elif child.tag in self.bitstruct_types:
                #     self.read_bitstruct(child)
                # elif child.tag == "basic":
                #     self.write_basic(child)
                elif child.tag == "enum":
                    Enum(self, child)
                elif child.tag == "bitfield":
                    # self.write_bitfield(child)
                    Bitfield(self, child)
                # elif child.tag == "bitflags":
                #     self.write_bitflags(child)
                # elif child.tag == "module":
                #     self.read_module(child)
                # elif child.tag == "version":
                #     self.read_version(child)
                elif child.tag == "token":
                    self.read_token(child)
            except Exception as err:
                logging.error(err)
                traceback.print_exc()
        logging.info(self.storage_types)

    # the following constructs do not create classes
    def read_token(self, token):
        """Reads an xml <token> block and stores it in the tokens list"""
        self.tokens.append(([(sub_token.attrib["token"], sub_token.attrib["string"])
                            for sub_token in token],
                            token.attrib["attrs"].split(" ")))
        
    def read_version(self, version):
        """Reads an xml <version> block and stores it in the versions list"""
        # todo [versions] this ignores the user vers!
        # versions must be in reverse order so don't append but insert at beginning
        if "id" in version.attrib:
            self.versions[0][0].insert( 0, (version.attrib["id"], version.attrib["num"]) )
        # add to supported versions
        self.version_string = version.attrib["num"]
        self.cls.versions[self.version_string] = self.cls.version_number(self.version_string)
        self.update_gamesdict(self.cls.games, version.text)
        self.version_string = None

    @staticmethod
    def get_names(struct):
        # struct types can be organized in a hierarchy
        # if inherit attribute is defined, look for corresponding base block
        class_name = convention.name_class(struct.attrib.get("name"))
        class_basename = struct.attrib.get("inherit")
        class_debug_str = clean_comment_str(struct.text, indent="\t")
        if class_basename:
            # avoid turning None into 'None' if class doesn't inherit
            class_basename = convention.name_class(class_basename)
            # logging.debug(f"Struct {class_name} is based on {class_basename}")
        return class_name, class_basename, class_debug_str

    def get_out_path(self, class_name):

        # get the module path from the path of the file
        out_file = os.path.join(os.getcwd(), "generated", self.path_dict[class_name]+".py")
        out_dir = os.path.dirname(out_file)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        return out_file

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

        # filter comment str
        struct.text = clean_comment_str(struct.text, indent="\t", class_comment='"""')

    def collect_types(self, imports, struct):
        """Iterate over all fields in struct and collect type references"""
        # import classes used in the fields
        for field in struct:
            if field.tag in ("add", "field", "member"):
                field_type = convention.name_class(field.attrib["type"])
                if field_type not in imports:
                    if field_type == "self.template":
                        imports.append("typing")
                    else:
                        imports.append(field_type)

    def write_imports(self, f, imports):
        for class_import in imports:
            if class_import in self.path_dict:
                import_path = "generated."+self.path_dict[class_import].replace("\\", ".")
                f.write(f"from {import_path} import {class_import}\n")
            else:
                f.write(f"import {class_import}\n")

    def method_for_type(self, dtype: str, mode="read", attr="self.dummy", arr1=None, arg=None):
        args = ""
        if arg:
            args = f", ({arg},)"
        # template or custom type
        if "template" in dtype.lower() or self.tag_dict[dtype.lower()] != "basic":
            io_func = f"{mode}_type"
        # basic type
        else:
            io_func = f"{mode}_{dtype.lower()}"
            dtype = ""
        if not arr1:
            if mode == "read":
                return f"{attr} = stream.{io_func}({dtype}{args})"
            elif mode == "write":
                return f"stream.{io_func}({attr})"
        else:
            arr1 = Expression(arr1)
            if mode == "read":
                return f"{attr} = [stream.{io_func}({dtype}{args}) for _ in range({arr1})]"
            elif mode == "write":
                return f"for item in {attr}: stream.{io_func}(item)"

            # todo - handle array 2
            # f.write(f"{indent}self.{field_name} = [{field_type}({template_str}) for _ in range({arr1})]")
        #     f.write(f"{indent}for item in self.{field_name}:")
        #     f.write(f"{indent}\titem.{method_type}(stream)")
        # return # f.write(f"{indent}self.{field_name} = {field_type}().{method_type}(stream)")
            # raise ModuleNotFoundError(f"Storage {dtype} is not a basic type.")
        # array of basic
        # if num_bones:
        #     self.bone_data = [stream.read_type(NiSkinDataBoneData) for _ in range(num_bones)]

    def write_bitflags(self, element: ElementTree.Element):
        class_name = convention.name_class(element.attrib['name'])
        out_file = os.path.join(os.getcwd(), "generated", self.path_dict[class_name]+".py")
        write_file(out_file, env.get_template('bitflags.py.jinja').render(bitflags=element))

    def write_bitfield(self, element: ElementTree.Element):
        class_name, class_basename, class_debug_str = self.get_names(element)

        out_file = self.get_out_path(class_name)
        storage = element.attrib["storage"]
        self.storage_types.add(storage)
        imports = ["BasicBitfield", "BitfieldMember"]
        dummy_imports = []
        self.collect_types(dummy_imports, element)
        for in_type in dummy_imports:
            must_import, in_type = self.map_type(in_type)
            if must_import:
                imports.append(in_type)
        # write to python file
        with open(out_file, "w") as f:
            self.write_imports(f, imports)

            if imports:
                f.write("\n\n")
            f.write(f"class {class_name}(BasicBitfield):")
            if class_debug_str:
                f.write(class_debug_str)

            for field in element:
                field_name = convention.name_attribute(field.attrib["name"])
                _, field_type = self.map_type(convention.name_class(field.attrib["type"]))
                f.write(f"\n\t{field_name} = BitfieldMember(pos={field.attrib['pos']}, mask={field.attrib['mask']}, return_type={field_type})")

            f.write("\n\n\tdef set_defaults(self):")
            defaults = []
            for field in element:
                field_name = convention.name_attribute(field.attrib["name"])
                field_type = convention.name_class(field.attrib["type"])
                field_default = field.attrib.get("default")
                # write the field's default, if it exists
                if field_default:
                    # we have to check if the default is an enum default value, in which case it has to be a member of that enum
                    if self.tag_dict[field_type.lower()] == "enum":
                        field_default = field_type+"."+field_default
                    defaults.append((field_name, field_default))
            if defaults:
                for field_name, field_default in defaults:
                    f.write(f"\n\t\tself.{field_name} = {field_default}")
            else:
                f.write(f"\n\t\tpass")

            self.write_storage_io_methods(f, storage)

            f.write("\n")

    def write_storage_io_methods(self, f, storage, attr='self._value'):
        for method_type in ("read", "write"):
            f.write(f"\n\n\tdef {method_type}(self, stream):")
            f.write(f"\n\t\t{self.method_for_type(storage, mode=method_type, attr=attr)}")
            # f.write(f"\n")

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

    def update_gamesdict(self, gamesdict, ver_text):
        if ver_text:
            # update the gamesdict dictionary
            for gamestr in (g.strip() for g in ver_text.split(',')):
                if gamestr in gamesdict:
                    gamesdict[gamestr].append(self.cls.versions[self.version_string])
                else:
                    gamesdict[gamestr] = [self.cls.versions[self.version_string]]
            
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
        # onlyT & excludeT act as aliases for deprecated cond
        for t, pref in (("onlyT", ""), ("excludeT", "!")):
            if t in xml_struct.attrib:
                xml_struct.attrib["cond"] = pref+xml_struct.attrib[t]
                break
        for xml_child in xml_struct:
            self.replace_tokens(xml_child)


def copy_src_to_generated():
    """copies the files from the source folder to the generated folder"""
    cwd = os.getcwd()
    src_dir = os.path.join(cwd, "source")
    trg_dir = os.path.join(cwd, "generated")
    copy_tree(src_dir, trg_dir)


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


generate_classes()