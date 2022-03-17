from generated.context import ContextReference
from generated.formats.dinosaurmaterialvariants.compound.Pointer import Pointer


class DinoVariantsHeader:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.name = Pointer(self.context, None, ZString)
		self.has_sets = 0
		self.set_name = Pointer(self.context, None, ZString)
		self.variants = Pointer(self.context, self.variant_count, VariantArray)
		self.variant_count = 0
		self.zero = 0
		self.set_defaults()

	def set_defaults(self):
		self.name = Pointer(self.context, None, ZString)
		self.has_sets = 0
		self.set_name = Pointer(self.context, None, ZString)
		self.variants = Pointer(self.context, self.variant_count, VariantArray)
		self.variant_count = 0
		self.zero = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.name = stream.read_type(Pointer, (self.context, None, ZString))
		self.has_sets = stream.read_uint64()
		self.set_name = stream.read_type(Pointer, (self.context, None, ZString))
		self.variants = stream.read_type(Pointer, (self.context, self.variant_count, VariantArray))
		self.variant_count = stream.read_uint64()
		self.zero = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.name)
		stream.write_uint64(self.has_sets)
		stream.write_type(self.set_name)
		stream.write_type(self.variants)
		stream.write_uint64(self.variant_count)
		stream.write_uint64(self.zero)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'DinoVariantsHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* name = {self.name.__repr__()}'
		s += f'\n	* has_sets = {self.has_sets.__repr__()}'
		s += f'\n	* set_name = {self.set_name.__repr__()}'
		s += f'\n	* variants = {self.variants.__repr__()}'
		s += f'\n	* variant_count = {self.variant_count.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
