from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
import logging


class FormatDict(dict):

	def __init__(self):
		super().__init__()

		# iterate through the modules in the current package
		package_dir = Path(__file__).resolve().parent
		for (_, module_name, _) in iter_modules([package_dir]):
			# import the module and iterate through its attributes
			try:
				module = import_module(f"modules.formats.{module_name}")
				for attribute_name in dir(module):
					attribute = getattr(module, attribute_name)

					if attribute_name in ("MemStructLoader", "BaseFile"):
						continue
					if isclass(attribute):
						# ignore any imports
						if not hasattr(attribute, "extension"):
							continue
						if attribute.extension is None:
							logging.debug(f"Missing extension on class {attribute_name} in file {module_name}")
							continue
						if not attribute.extension.startswith("."):
							logging.warning(f"Bad extension '{attribute.extension}' on class {attribute_name} in file {module_name}")
							continue
						# register
						self[attribute.extension] = attribute
						# also store alternative file extensions
						for alias in attribute.aliases:
							self[alias] = attribute
			except ModuleNotFoundError:
				logging.exception(f"Could not load {module_name}")

	@property
	def extractables(self):
		return [ext for ext, loader in self.items() if loader.can_extract]

	@property
	def ignore_types(self):
		return [ext for ext, loader in self.items() if not loader.can_extract]
