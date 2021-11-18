from generated.context import ContextReference


class Root1Pad:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.zero_2 = 0
		self.zero_3 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.zero_0 = 0
		self.zero_1 = 0
		self.zero_2 = 0
		self.zero_3 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.zero_0 = stream.read_uint()
		self.zero_1 = stream.read_uint()
		self.zero_2 = stream.read_uint()
		self.zero_3 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.zero_0)
		stream.write_uint(self.zero_1)
		stream.write_uint(self.zero_2)
		stream.write_uint(self.zero_3)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Root1Pad [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zero_0 = {self.zero_0.__repr__()}'
		s += f'\n	* zero_1 = {self.zero_1.__repr__()}'
		s += f'\n	* zero_2 = {self.zero_2.__repr__()}'
		s += f'\n	* zero_3 = {self.zero_3.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
