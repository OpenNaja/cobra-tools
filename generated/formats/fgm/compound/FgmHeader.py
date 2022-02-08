from generated.context import ContextReference


class FgmHeader:

	"""
	Sized str entry of 16 bytes, then ptrs, then padding
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.texture_count = 0
		self.texture_count = 0
		self.attribute_count = 0
		self.attribute_count = 0
		self.tex_ptr = 0
		self.attr_ptr = 0
		self.dependencies_ptr = 0
		self.data_ptr = 0
		self.unk_0 = 0
		self.unk_1 = 0
		self.set_defaults()

	def set_defaults(self):
		if self.context.version <= 15:
			self.texture_count = 0
		if self.context.version >= 17:
			self.texture_count = 0
		if self.context.version <= 15:
			self.attribute_count = 0
		if self.context.version >= 17:
			self.attribute_count = 0
		self.tex_ptr = 0
		self.attr_ptr = 0
		self.dependencies_ptr = 0
		self.data_ptr = 0
		self.unk_0 = 0
		self.unk_1 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		if self.context.version <= 15:
			self.texture_count = stream.read_uint()
		if self.context.version >= 17:
			self.texture_count = stream.read_uint64()
		if self.context.version <= 15:
			self.attribute_count = stream.read_uint()
		if self.context.version >= 17:
			self.attribute_count = stream.read_uint64()
		self.tex_ptr = stream.read_uint64()
		self.attr_ptr = stream.read_uint64()
		self.dependencies_ptr = stream.read_uint64()
		self.data_ptr = stream.read_uint64()
		self.unk_0 = stream.read_uint64()
		self.unk_1 = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		if self.context.version <= 15:
			stream.write_uint(self.texture_count)
		if self.context.version >= 17:
			stream.write_uint64(self.texture_count)
		if self.context.version <= 15:
			stream.write_uint(self.attribute_count)
		if self.context.version >= 17:
			stream.write_uint64(self.attribute_count)
		stream.write_uint64(self.tex_ptr)
		stream.write_uint64(self.attr_ptr)
		stream.write_uint64(self.dependencies_ptr)
		stream.write_uint64(self.data_ptr)
		stream.write_uint64(self.unk_0)
		stream.write_uint64(self.unk_1)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'FgmHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* texture_count = {self.texture_count.__repr__()}'
		s += f'\n	* attribute_count = {self.attribute_count.__repr__()}'
		s += f'\n	* tex_ptr = {self.tex_ptr.__repr__()}'
		s += f'\n	* attr_ptr = {self.attr_ptr.__repr__()}'
		s += f'\n	* dependencies_ptr = {self.dependencies_ptr.__repr__()}'
		s += f'\n	* data_ptr = {self.data_ptr.__repr__()}'
		s += f'\n	* unk_0 = {self.unk_0.__repr__()}'
		s += f'\n	* unk_1 = {self.unk_1.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
