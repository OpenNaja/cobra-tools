class DataPointer:

# second Section of a soundback aux
	wem_id: int

	# offset into data section
	data_section_offset: int

	# length of the wem file
	wem_filesize: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.wem_id = stream.read_uint()
		self.data_section_offset = stream.read_uint()
		self.wem_filesize = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self.wem_id)
		stream.write_uint(self.data_section_offset)
		stream.write_uint(self.wem_filesize)

	def __repr__(self):
		s = 'DataPointer'
		s += '\n	* wem_id = ' + self.wem_id.__repr__()
		s += '\n	* data_section_offset = ' + self.data_section_offset.__repr__()
		s += '\n	* wem_filesize = ' + self.wem_filesize.__repr__()
		s += '\n'
		return s