from generated.context import ContextReference
from generated.formats.matcol.compound.Info import Info


class InfoWrapper:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.info = Info(self.context, None, None)
		self.name = 0
		self.set_defaults()

	def set_defaults(self):
		self.info = Info(self.context, None, None)
		self.name = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.info = stream.read_type(Info, (self.context, None, None))
		self.name = stream.read_zstring()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.info)
		stream.write_zstring(self.name)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'InfoWrapper [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* info = {self.info.__repr__()}'
		s += f'\n	* name = {self.name.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
