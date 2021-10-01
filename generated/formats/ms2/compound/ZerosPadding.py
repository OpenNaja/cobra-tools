from generated.context import ContextReference


class ZerosPadding:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.hier_2_padding_0 = 0

		# 128 still has 16 bytes
		self.hier_2_padding_1 = 0

		# 129 is the first with 24 bytes
		self.hier_2_padding_2 = 0
		self.set_defaults()

	def set_defaults(self):
		self.hier_2_padding_0 = 0
		if 64 < self.arg:
			self.hier_2_padding_1 = 0
		if 128 < self.arg:
			self.hier_2_padding_2 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.hier_2_padding_0 = stream.read_uint64()
		if 64 < self.arg:
			self.hier_2_padding_1 = stream.read_uint64()
		if 128 < self.arg:
			self.hier_2_padding_2 = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64(self.hier_2_padding_0)
		if 64 < self.arg:
			stream.write_uint64(self.hier_2_padding_1)
		if 128 < self.arg:
			stream.write_uint64(self.hier_2_padding_2)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ZerosPadding [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* hier_2_padding_0 = {self.hier_2_padding_0.__repr__()}'
		s += f'\n	* hier_2_padding_1 = {self.hier_2_padding_1.__repr__()}'
		s += f'\n	* hier_2_padding_2 = {self.hier_2_padding_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
