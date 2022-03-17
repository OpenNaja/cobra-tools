from generated.context import ContextReference
from generated.formats.dinosaurmaterialvariants.compound.Pointer import Pointer


class Variant:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.has_ptr = 0
		self.name = Pointer(self.context, None, ZString)
		self.set_defaults()

	def set_defaults(self):
		self.has_ptr = 0
		self.name = Pointer(self.context, None, ZString)

	def read(self, stream):
		self.io_start = stream.tell()
		self.has_ptr = stream.read_uint64()
		self.name = stream.read_type(Pointer, (self.context, None, ZString))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64(self.has_ptr)
		stream.write_type(self.name)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Variant [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* has_ptr = {self.has_ptr.__repr__()}'
		s += f'\n	* name = {self.name.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
