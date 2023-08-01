import sys
import ast
from pathlib import Path
from dataclasses import dataclass
from functools import cached_property
from typing import Any, Generator


class ModuleSource:
	BUILTIN = 'BUILTIN'
	TYPING = 'TYPING'
	THIRD_PARTY = 'THIRD_PARTY'
	APPLICATION = 'APPLICATION'


@dataclass(frozen=True)
class Import:
	node: ast.Import | ast.ImportFrom

	STATIC_SOURCES = {
		'__future__': ModuleSource.BUILTIN,
		'__main__': ModuleSource.APPLICATION,
		'distutils': ModuleSource.THIRD_PARTY,
		'typing': ModuleSource.TYPING,
		'': ModuleSource.APPLICATION, # relative imports
	}

	@cached_property
	def module(self) -> str:
		level = ""
		if isinstance(self.node, ast.ImportFrom):
			level = '.' * self.node.level  # Locals
			mod = self.node.module or ''
			return f'{level}{mod}'
		return self.node.names[0].name
	
	@cached_property
	def modules(self) -> list[str]:
		if isinstance(self.node, ast.Import):
			return [n.name for n in self.node.names]
		elif isinstance(self.node, ast.ImportFrom):
			level = self.node.level * "."  # Locals
			return self.node.module.split('.') if self.node.module else [level]
		return []

	@cached_property
	def module_base(self) -> str:
		return self.module.partition('.')[0]

	@cached_property
	def module_source(self) -> str:
		if self.module_base in Import.STATIC_SOURCES.keys():
			return Import.STATIC_SOURCES[self.module_base]
		elif self.module_base in sys.stdlib_module_names:
			return ModuleSource.BUILTIN
		elif Import.is_local(self.module_base):
			return ModuleSource.APPLICATION
		else:
			return ModuleSource.THIRD_PARTY
		
	@cached_property
	def name(self) -> str:
		return self.node.names[0].name
	
	@cached_property
	def names(self) -> list[str]:
		return [Import.alias_to_str(name) for name in self.node.names]

	@staticmethod
	def alias_to_str(node: ast.alias) -> str:
		if node.asname:
			return f'{node.name} as {node.asname}'
		else:
			return node.name

	@staticmethod
	def is_local(base: str) -> bool:
		basepath = Path('.').joinpath(base)
		return (basepath.with_suffix(".py").exists() 
				or (basepath.exists() and basepath.is_dir() and basepath.glob("__init__.py")))

	def __str__(self) -> str:
		from_str = ""
		if isinstance(self.node, ast.ImportFrom):
			from_str = f'from {self.module} '
		return f"{from_str}import {', '.join(self.names)}"


def get_imports(path) -> Generator[Import, Any, None]:
	with open(path) as fh:
		root = ast.parse(fh.read(), path)

	for node in ast.walk(root):
		if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
			yield Import(node)
