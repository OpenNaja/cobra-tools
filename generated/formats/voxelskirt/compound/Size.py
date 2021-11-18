from generated.context import ContextReference


class Size:

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
		self.width_1 = 0
		self.height_1 = 0
		self.width_2 = 0
		self.height_2 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.id = 0
		self.width_1 = 0
		self.height_1 = 0
		self.width_2 = 0
		self.height_2 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.id = stream.read_uint64()
		self.width_1 = stream.read_uint64()
		self.height_1 = stream.read_uint64()
		self.width_2 = stream.read_uint64()
		self.height_2 = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64(self.id)
		stream.write_uint64(self.width_1)
		stream.write_uint64(self.height_1)
		stream.write_uint64(self.width_2)
		stream.write_uint64(self.height_2)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Size [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* id = {self.id.__repr__()}'
		s += f'\n	* width_1 = {self.width_1.__repr__()}'
		s += f'\n	* height_1 = {self.height_1.__repr__()}'
		s += f'\n	* width_2 = {self.width_2.__repr__()}'
		s += f'\n	* height_2 = {self.height_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
