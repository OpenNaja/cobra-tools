from .BaseClass import BaseClass

FIELD_TYPES = ("add", "field")
VER = "stream.version"


class Enum(BaseClass):

	def read(self):
		"""Create a struct class"""
		super().read()

		storage = self.struct.attrib["storage"]
		# todo - handle case where storage is given as size instead of name
		# store storage format in dict so it can be accessed during compound writing
		self.parser.storage_dict[self.class_name] = storage
		enum_base = f"{storage.capitalize()}Enum"
		self.class_basename = enum_base
		self.imports.add(enum_base)
		# write to python file
		with open(self.out_file, "w") as f:
			# write the header stuff
			super().write(f)
			for option in self.struct:
				if option.text:
					f.write(f"\n\t# {option.text}")
				f.write(f"\n\t{option.attrib['name']} = {option.attrib['value']}")
			# self.parser.write_storage_io_methods(f, storage, attr='self._value_')
			f.write(f"\n")
