from generated.context import ContextReference
from generated.formats.bnk.compound.Type2 import Type2
from generated.formats.bnk.compound.TypeOther import TypeOther


class HircPointer:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of following data
		self.id = 0
		self.data = Type2(self.context, 0, None)
		self.data = TypeOther(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.id = 0
		if self.id == 2:
			self.data = Type2(self.context, 0, None)
		if self.id != 2:
			self.data = TypeOther(self.context, 0, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.id = stream.read_byte()
		if self.id == 2:
			self.data = stream.read_type(Type2, (self.context, 0, None))
		if self.id != 2:
			self.data = stream.read_type(TypeOther, (self.context, 0, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_byte(self.id)
		if self.id == 2:
			stream.write_type(self.data)
		if self.id != 2:
			stream.write_type(self.data)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'HircPointer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* id = {self.id.__repr__()}'
		s += f'\n	* data = {self.data.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
