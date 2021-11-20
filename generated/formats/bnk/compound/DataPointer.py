from generated.context import ContextReference


class DataPointer:

	"""
	second Section of a soundback aux
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.wem_id = 0

		# offset into data section
		self.data_section_offset = 0

		# length of the wem file
		self.wem_filesize = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
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

	def get_info_str(self):
		return f'DataPointer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* wem_id = {self.wem_id.__repr__()}'
		s += f'\n	* data_section_offset = {self.data_section_offset.__repr__()}'
		s += f'\n	* wem_filesize = {self.wem_filesize.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
