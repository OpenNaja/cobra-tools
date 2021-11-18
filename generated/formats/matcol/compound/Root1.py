from generated.context import ContextReference


class Root1:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.flag = 0
		self.zero_1 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.flag = 0
		self.zero_1 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.flag = stream.read_uint()
		self.zero_1 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.flag)
		stream.write_uint(self.zero_1)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Root1 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* flag = {self.flag.__repr__()}'
		s += f'\n	* zero_1 = {self.zero_1.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
