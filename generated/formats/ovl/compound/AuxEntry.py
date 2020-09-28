class AuxEntry:

# describes an external AUX resource

	# index into files list
	file_index: int

	# maybe index into extension list
	extension_index: int

	# byte count of the complete external resource file
	size: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.file_index = 0
		self.extension_index = 0
		self.size = 0

	def read(self, stream):
		self.file_index = stream.read_uint()
		self.extension_index = stream.read_uint()
		self.size = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self.file_index)
		stream.write_uint(self.extension_index)
		stream.write_uint(self.size)

	def __repr__(self):
		s = 'AuxEntry'
		s += '\n	* file_index = ' + self.file_index.__repr__()
		s += '\n	* extension_index = ' + self.extension_index.__repr__()
		s += '\n	* size = ' + self.size.__repr__()
		s += '\n'
		return s