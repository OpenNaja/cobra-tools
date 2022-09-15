import ast
import os
import re
import sys

from root_path import root_dir
from .Imports import Imports


keyword_regex = re.compile(r"(\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[a-zA-Z_][a-zA-Z0-9_]*)")


class BaseClass:

    def __init__(self, parser, struct):
        self.parser = parser
        self.struct = struct
        self.read()

    def read(self, ):
        self.class_name = self.struct.attrib.get("name")
        # grab the source code, if it exists
        self.src_code = self.get_code_from_src()
        self.class_basename = self.struct.attrib.get("inherit")
        self.class_debug_str = self.struct.text
        self.out_file = self.get_out_path(self.parser.path_dict[self.class_name])

        # handle imports
        self.imports = Imports(self.parser, self.struct)

    def get_class_call(self):
        # set backup
        inheritance = f"({self.class_basename})" if self.class_basename else ""
        class_call = f"class {self.class_name}{inheritance}:"
        if (sys.version_info.major, sys.version_info.minor) >= (3, 9):
            # if python version >= 3.9, use ast, because it's more robust
            src_ast = ast.parse(self.src_code, type_comments=True)
            if self.src_code:
                found_classes = [ast_node for ast_node in src_ast.body if isinstance(ast_node, ast.ClassDef) and ast_node.name == self.class_name]
                if found_classes:
                    found_class = found_classes[-1]
                    found_class.body[:] = [ast.Pass()]
                    if not any(getattr(base_class, "id", None) == self.class_basename for base_class in found_class.bases):
                        # the inherit class is not yet in the bases, add it
                        found_class.bases.append(ast.Name(id=self.class_basename, ctx=ast.Load()))
                        class_call = ast.unparse(found_class)
                        # trim the parse that was set as the body
                        class_call = class_call[:class_call.rfind(":") + 1]
        else:
            # use regex as a second-best alternative
            existing_class_call = re.search(fr"(class {self.class_name})(\(.*\))?\:", self.src_code)
            if existing_class_call:
                existing_arguments = existing_class_call.group(2)
                if existing_arguments:
                    if re.search(fr"[\(,]\s*{self.class_basename}\s*[\),]", existing_arguments):
                        # inherit class already in the class call, no futher action required
                        class_call = existing_class_call.group(0)
                    else:
                        # find the first keyword argument and put the inherit class before that
                        keyword_match = keyword_regex.search(existing_arguments)
                        if keyword_match:
                            left = existing_arguments[:keyword_match.start]
                            right = existing_arguments[keyword_match.start:]
                        else:
                            # there are no keyword arguments in the class call, put it last
                            left = existing_arguments[:-1]
                            right = existing_arguments[-1:]
                        total_arguments = f"{left}{', ' if left[1:].strip() else ''}{self.class_basename}{', ' if right[:-1].strip() else ''}{right}"
                        class_call = f"class {self.class_name}{total_arguments}:"

        return class_call

    def write(self, stream):
        src_globals = self.grab_src_snippet("# START_GLOBALS", "# END_GLOBALS")
        src_globals = "\n".join(src_globals.split("\n")[1:])
        stream.write(src_globals)

        self.imports.write(stream)

        class_call = self.get_class_call()
        stream.write(class_call)
        if self.class_debug_str:
            stream.write(self.class_debug_str)
        self.write_line(stream)
        self.write_line(stream, 1, f"__name__ = '{self.struct.attrib.get('__name__')}'")

    def write_line(self, stream, indent=0, line=""):
        stream.write("\n" + indent*"\t" + line)

    def write_lines(self, stream, indent, lines):
        for line in lines:
            self.write_line(stream, indent, line)

    def get_code_from_src(self,):
        src_dir = os.path.join(root_dir, "source")
        py_name = f"{self.class_name.lower()}.py"

        for root, dirs, files in os.walk(src_dir, followlinks=True):
            for name in files:
                if self.parser.format_name in root and py_name == name.lower():
                    src_path = os.path.join(root, name)
                    # print(f"found source {src_path}")
                    with open(src_path, "r", encoding=self.parser.encoding) as f:
                        return f.read()
        return ""

    def grab_src_snippet(self, start, end=""):
        # print(src_code)
        start_content = self.src_code.find(start)
        if start_content > -1:
            if end:
                end_content = self.src_code.find(end)
                if end_content > -1:
                    snipp = self.src_code[start_content + len(start):end_content]
                    # print("found start + end", len(snipp), start, end)
                    return snipp
            snipp = self.src_code[start_content + len(start):]
            # print("found start", len(snipp), start, end)
            return snipp
        return ""

    @staticmethod
    def get_out_path(module_path):
        # get the module path from the path of the file
        out_file = os.path.join(root_dir, "generated", module_path + ".py")
        out_dir = os.path.dirname(out_file)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        return out_file
