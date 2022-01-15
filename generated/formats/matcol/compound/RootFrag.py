from generated.context import ContextReference


class RootFrag:

	"""
	mat_type, ptr0, tex_count, ptr1, mat_count, ptr2
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.mat_type = 0
		self.ptr_0 = 0
		self.tex_count = 0
		self.ptr_1 = 0
		self.mat_count = 0
		self.ptr_2 = 0
		self.set_defaults()

	def set_defaults(self):
		self.mat_type = 0
		self.ptr_0 = 0
		self.tex_count = 0
		self.ptr_1 = 0
		self.mat_count = 0
		self.ptr_2 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.mat_type = stream.read_uint64()
		self.ptr_0 = stream.read_uint64()
		self.tex_count = stream.read_uint64()
		self.ptr_1 = stream.read_uint64()
		self.mat_count = stream.read_uint64()
		self.ptr_2 = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64(self.mat_type)
		stream.write_uint64(self.ptr_0)
		stream.write_uint64(self.tex_count)
		stream.write_uint64(self.ptr_1)
		stream.write_uint64(self.mat_count)
		stream.write_uint64(self.ptr_2)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'RootFrag [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* mat_type = {self.mat_type.__repr__()}'
		s += f'\n	* ptr_0 = {self.ptr_0.__repr__()}'
		s += f'\n	* tex_count = {self.tex_count.__repr__()}'
		s += f'\n	* ptr_1 = {self.ptr_1.__repr__()}'
		s += f'\n	* mat_count = {self.mat_count.__repr__()}'
		s += f'\n	* ptr_2 = {self.ptr_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
