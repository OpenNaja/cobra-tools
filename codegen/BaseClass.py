import ast
import logging
import os
import re
from functools import lru_cache
from typing import TYPE_CHECKING, Iterable, Iterator, TextIO

from .path_utils import module_path_to_file_path, to_import_path
from .Imports import Imports
if TYPE_CHECKING:
    from . import Config, Element
    from .XmlParser import XmlParser


keyword_regex: re.Pattern[str] = re.compile(r"(\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[a-zA-Z_][a-zA-Z0-9_]*)")


class BaseClass:

    def __init__(self, parser: 'XmlParser', struct: 'Element', cfg: 'Config'):
        self.parser: XmlParser = parser
        self.struct: 'Element' = struct
        self.gen_dir: str = cfg.gen_dir
        self.src_dir: str = cfg.src_dir
        self.root_dir: str = cfg.root_dir
        self.write_stubs: bool = cfg.write_stubs
        self.read()

    @property
    def elements(self) -> Iterator['Element']:
        """A generator that yields only the true XML elements, filtering out comments."""
        return (child for child in self.struct if isinstance(child.tag, str))

    def read(self, ) -> None:
        self.class_name: str | None = self.struct.attrib.get("name")
        if not self.class_name:
            logging.warning(f"XML element <{self.struct.tag}> is missing required 'name' attribute, skipping.")
            return
        # grab the source code, if it exists
        self.src_code: str = self.get_code_from_src()
        if self.src_code.find("START_GLOBALS") == -1 and self.src_code.find("from generated.") > -1:
            logging.error(f"{self.class_name} does not wrap imports with START_GLOBALS/END_GLOBALS")
        self.class_basename = self.struct.attrib.get("inherit")
        if self.class_basename is not None and self.class_basename not in self.parser.processed_types:
            logging.error(f"Class {self.class_name} in format {self.parser.format_name} inherits from "\
                         f"{self.class_basename}, but this is not declared in the xml before it!")
        self.class_debug_str: str | None = self.struct.text
        self.out_file: str = module_path_to_file_path(self.parser.path_dict[self.class_name], self.gen_dir, self.root_dir)
        self.out_pyi_file: str = os.path.splitext(self.out_file)[0] + ".pyi"

        # handle imports
        self.imports = Imports(self.parser, self.struct, gen_dir=self.gen_dir)

        self.parser.processed_types[self.class_name] = None

    @lru_cache(maxsize=None)
    def get_class_call(self) -> str:
        """
        Generates the class definition line (e.g., 'class MyClass(Base):').
        """
        # Define a fallback value in case AST parsing fails or the class isn't found
        inheritance = f"({self.class_basename})" if self.class_basename else ""
        fallback_call = f"class {self.class_name}{inheritance}:"
        if not self.src_code:
            return fallback_call
        try:
            src_ast = ast.parse(self.src_code, type_comments=True)
        except SyntaxError:
            logging.error(f"[get_class_call] Invalid source code, falling back to '{fallback_call}'")
            return fallback_call
        # Find the last definition of the class in the source file
        class_node = next((node for node in reversed(src_ast.body)
                           if isinstance(node, ast.ClassDef) and node.name == self.class_name),
                          None)
        if not class_node:
            return fallback_call
        # If a base class is specified, ensure it's in the AST node's bases.
        if self.class_basename:
            # Check if the base class is already present.
            has_base_class = any(getattr(base, "id", None) == self.class_basename
                                 for base in class_node.bases)
            if not has_base_class:
                class_node.bases.append(ast.Name(id=self.class_basename, ctx=ast.Load()))
        # Replace the class body with 'pass'
        class_node.body = [ast.Pass()]
        # Re-generate the source code from the modified AST node.
        class_call_str = ast.unparse(class_node)
        # Trim the generated string to get just the class definition line.
        # The rfind(':') is a robust way to handle multi-line class definitions.
        return class_call_str[:class_call_str.rfind(":") + 1]

    def write(self, stream: TextIO) -> None:
        src_globals: str = self.grab_src_snippet("# START_GLOBALS", "# END_GLOBALS")
        src_globals = "\n".join(src_globals.split("\n")[1:])
        src_globals = src_globals.replace("from generated.", f"from {to_import_path(self.gen_dir)}.")
        src_globals = src_globals.replace("import generated.", f"import {to_import_path(self.gen_dir)}.")
        stream.write(src_globals)

        self.imports.write(stream)

        class_call: str = self.get_class_call()
        stream.write(class_call)
        if self.class_debug_str:
            stream.write(self.class_debug_str)
        self.write_line(stream)
        self.write_line(stream, 1, f"__name__ = '{self.struct.attrib.get('__name__')}'")

    def write_src_body(self, stream: TextIO) -> None:
        stream.write(self.grab_src_snippet("# START_CLASS"))

    def write_line(self, stream: TextIO, indent: int = 0, line: str = "") -> None:
        stream.write("\n" + indent*"\t" + line)

    def write_lines(self, stream: TextIO, indent: int, lines: Iterable[str]) -> None:
        for line in lines:
            self.write_line(stream, indent, line)

    def get_code_from_src(self,) -> str:
        if not self.class_name:
            return ""
        src_file: str = module_path_to_file_path(self.parser.path_dict[self.class_name], self.src_dir, self.root_dir, mkdir=False)
        if os.path.exists(src_file):
            with open(src_file, "r", encoding=self.parser.encoding) as f:
                return f.read()
        return ""

    def grab_src_snippet(self, start: str, end: str = "") -> str:
        # print(src_code)
        start_content: int = self.src_code.find(start)
        if start_content > -1:
            if end:
                end_content = self.src_code.find(end)
                if end_content > -1:
                    snipp: str = self.src_code[start_content + len(start):end_content]
                    # print("found start + end", len(snipp), start, end)
                    return snipp
            return self.src_code[start_content + len(start):]
        return ""
