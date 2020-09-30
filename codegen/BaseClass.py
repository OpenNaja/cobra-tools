import os
from .Imports import Imports
from . import naming_conventions as convention

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
        self.out_file = self.parser.get_out_path(self.class_name)

        # handle imports
        self.imports = Imports(self.parser, self.struct)

    def write(self, stream):
        stream.write(self.grab_src_snippet("# START_GLOBALS", "# END_GLOBALS"))

        self.imports.write(stream)

        inheritance = f"({self.class_basename})" if self.class_basename else ""
        stream.write(f"class {self.class_name}{inheritance}:")
        if self.class_debug_str:
            stream.write(self.class_debug_str)

    def get_code_from_src(self,):
        cwd = os.getcwd()
        src_dir = os.path.join(cwd, "source")
        py_name = f"{self.class_name.lower()}.py"

        for root, dirs, files in os.walk(src_dir):
            for name in files:
                if self.parser.format_name in root and py_name == name.lower():
                    src_path = os.path.join(root, name)
                    print("found source", src_path)
                    with open(src_path, "r") as f:
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