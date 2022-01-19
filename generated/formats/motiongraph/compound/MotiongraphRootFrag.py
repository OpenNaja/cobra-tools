from generated.context import ContextReference
from generated.formats.motiongraph.compound.Pointer import Pointer


class MotiongraphRootFrag:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.count_0 = 0
		self.ptr_0 = Pointer(self.context, None, None)
		self.count_1 = 0
		self.ptr_1 = Pointer(self.context, None, None)
		self.count_2 = 0
		self.ptr_2 = Pointer(self.context, None, None)
		self.num_xmls = 0
		self.ptr_xmls = Pointer(self.context, None, None)
		self.set_defaults()

	def set_defaults(self):
		self.count_0 = 0
		self.ptr_0 = Pointer(self.context, None, None)
		self.count_1 = 0
		self.ptr_1 = Pointer(self.context, None, None)
		self.count_2 = 0
		self.ptr_2 = Pointer(self.context, None, None)
		self.num_xmls = 0
		self.ptr_xmls = Pointer(self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.count_0 = stream.read_uint64()
		self.ptr_0 = stream.read_type(Pointer, (self.context, None, None))
		self.count_1 = stream.read_uint64()
		self.ptr_1 = stream.read_type(Pointer, (self.context, None, None))
		self.count_2 = stream.read_uint64()
		self.ptr_2 = stream.read_type(Pointer, (self.context, None, None))
		self.num_xmls = stream.read_uint64()
		self.ptr_xmls = stream.read_type(Pointer, (self.context, None, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64(self.count_0)
		stream.write_type(self.ptr_0)
		stream.write_uint64(self.count_1)
		stream.write_type(self.ptr_1)
		stream.write_uint64(self.count_2)
		stream.write_type(self.ptr_2)
		stream.write_uint64(self.num_xmls)
		stream.write_type(self.ptr_xmls)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'MotiongraphRootFrag [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* count_0 = {self.count_0.__repr__()}'
		s += f'\n	* ptr_0 = {self.ptr_0.__repr__()}'
		s += f'\n	* count_1 = {self.count_1.__repr__()}'
		s += f'\n	* ptr_1 = {self.ptr_1.__repr__()}'
		s += f'\n	* count_2 = {self.count_2.__repr__()}'
		s += f'\n	* ptr_2 = {self.ptr_2.__repr__()}'
		s += f'\n	* num_xmls = {self.num_xmls.__repr__()}'
		s += f'\n	* ptr_xmls = {self.ptr_xmls.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
