from generated.context import ContextReference
from generated.formats.motiongraph.compound.Pointer import Pointer


class MotiongraphHeader:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.ptr_0 = Pointer(self.context, None, None)
		self.ptr_1 = Pointer(self.context, None, None)
		self.ptr_2 = Pointer(self.context, None, None)
		self.ptr_3 = Pointer(self.context, None, None)
		self.count_0 = 0
		self.count_1 = 0
		self.ptr_4 = Pointer(self.context, None, None)
		self.ptr_5 = Pointer(self.context, None, None)
		self.ptr_6 = Pointer(self.context, None, None)
		self.ptr_7 = Pointer(self.context, None, None)
		self.set_defaults()

	def set_defaults(self):
		self.ptr_0 = Pointer(self.context, None, None)
		self.ptr_1 = Pointer(self.context, None, None)
		self.ptr_2 = Pointer(self.context, None, None)
		self.ptr_3 = Pointer(self.context, None, None)
		self.count_0 = 0
		self.count_1 = 0
		self.ptr_4 = Pointer(self.context, None, None)
		self.ptr_5 = Pointer(self.context, None, None)
		self.ptr_6 = Pointer(self.context, None, None)
		self.ptr_7 = Pointer(self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.ptr_0 = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_1 = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_2 = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_3 = stream.read_type(Pointer, (self.context, None, None))
		self.count_0 = stream.read_uint()
		self.count_1 = stream.read_uint()
		self.ptr_4 = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_5 = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_6 = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_7 = stream.read_type(Pointer, (self.context, None, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.ptr_0)
		stream.write_type(self.ptr_1)
		stream.write_type(self.ptr_2)
		stream.write_type(self.ptr_3)
		stream.write_uint(self.count_0)
		stream.write_uint(self.count_1)
		stream.write_type(self.ptr_4)
		stream.write_type(self.ptr_5)
		stream.write_type(self.ptr_6)
		stream.write_type(self.ptr_7)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'MotiongraphHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* ptr_0 = {self.ptr_0.__repr__()}'
		s += f'\n	* ptr_1 = {self.ptr_1.__repr__()}'
		s += f'\n	* ptr_2 = {self.ptr_2.__repr__()}'
		s += f'\n	* ptr_3 = {self.ptr_3.__repr__()}'
		s += f'\n	* count_0 = {self.count_0.__repr__()}'
		s += f'\n	* count_1 = {self.count_1.__repr__()}'
		s += f'\n	* ptr_4 = {self.ptr_4.__repr__()}'
		s += f'\n	* ptr_5 = {self.ptr_5.__repr__()}'
		s += f'\n	* ptr_6 = {self.ptr_6.__repr__()}'
		s += f'\n	* ptr_7 = {self.ptr_7.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
