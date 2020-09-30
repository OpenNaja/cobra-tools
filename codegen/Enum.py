from .BaseClass import BaseClass

FIELD_TYPES = ("add", "field")
VER = "stream.version"


class Enum(BaseClass):

	def read(self):
		"""Create a self.struct class"""
		super().read()

		self.class_basename = "enum.IntEnum"
		self.imports.add("enum")
		# write to python file
		with open(self.out_file, "w") as f:
			# write the header stuff
			super().write(f)
			storage = self.struct.attrib["storage"]
			for option in self.struct:
				if option.text:
					f.write(f"\n\t# {option.text}")
				f.write(f"\n\t{option.attrib['name']} = {option.attrib['value']}")
			print(storage)
			self.parser.write_storage_io_methods(f, storage, attr='self._value_')
			f.write(f"\n")
