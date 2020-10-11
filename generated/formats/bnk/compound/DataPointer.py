class DataPointer:

	"""
	second Section of a soundback aux
	"""
	wem_id: int

	# offset into data section
	data_section_offset: int

	# length of the wem file
	wem_filesize: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.wem_id = 0
		self.data_section_offset = 0
		self.wem_filesize = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.wem_id = stream.read_uint()
		self.data_section_offset = stream.read_uint()
		self.wem_filesize = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.wem_id)
		stream.write_uint(self.data_section_offset)
		stream.write_uint(self.wem_filesize)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'DataPointer [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* wem_id = ' + self.wem_id.__repr__()
		s += '\n	* data_section_offset = ' + self.data_section_offset.__repr__()
		s += '\n	* wem_filesize = ' + self.wem_filesize.__repr__()
		s += '\n'
		return s
