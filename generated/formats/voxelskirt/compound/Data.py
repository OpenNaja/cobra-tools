from generated.context import ContextReference


class Data:

	"""
	PZ and JWE only, describes a data layer image
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# index into name list
		self.id = 0

		# 0 = ubyte, 2 = float
		self.type = 0

		# address of this data layer
		self.offset = 0

		# data size of this layer, in bytes
		self.dsize = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.id = 0
		self.type = 0
		self.offset = 0
		self.dsize = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.id = stream.read_uint64()
		self.type = stream.read_uint64()
		self.offset = stream.read_uint64()
		self.dsize = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64(self.id)
		stream.write_uint64(self.type)
		stream.write_uint64(self.offset)
		stream.write_uint64(self.dsize)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Data [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* id = {self.id.__repr__()}'
		s += f'\n	* type = {self.type.__repr__()}'
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* dsize = {self.dsize.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
