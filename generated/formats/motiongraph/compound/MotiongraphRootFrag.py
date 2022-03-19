from source.formats.base.basic import fmt_member
from generated.context import ContextReference
from generated.formats.motiongraph.compound.Pointer import Pointer


class MotiongraphRootFrag:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.num_xmls = 0
		self.ptr_0 = Pointer(self.context, 0, None)
		self.ptr_1 = Pointer(self.context, 0, None)
		self.ptr_2 = Pointer(self.context, 0, None)
		self.ptr_xmls = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.num_xmls = 0
		self.ptr_0 = Pointer(self.context, 0, None)
		self.ptr_1 = Pointer(self.context, 0, None)
		self.ptr_2 = Pointer(self.context, 0, None)
		self.ptr_xmls = Pointer(self.context, 0, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		instance.count_0 = stream.read_uint64()
		instance.ptr_0 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.count_1 = stream.read_uint64()
		instance.ptr_1 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.count_2 = stream.read_uint64()
		instance.ptr_2 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.num_xmls = stream.read_uint64()
		instance.ptr_xmls = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_0.arg = 0
		instance.ptr_1.arg = 0
		instance.ptr_2.arg = 0
		instance.ptr_xmls.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint64(instance.count_0)
		Pointer.to_stream(stream, instance.ptr_0)
		stream.write_uint64(instance.count_1)
		Pointer.to_stream(stream, instance.ptr_1)
		stream.write_uint64(instance.count_2)
		Pointer.to_stream(stream, instance.ptr_2)
		stream.write_uint64(instance.num_xmls)
		Pointer.to_stream(stream, instance.ptr_xmls)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'MotiongraphRootFrag [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* count_0 = {fmt_member(self.count_0, indent+1)}'
		s += f'\n	* ptr_0 = {fmt_member(self.ptr_0, indent+1)}'
		s += f'\n	* count_1 = {fmt_member(self.count_1, indent+1)}'
		s += f'\n	* ptr_1 = {fmt_member(self.ptr_1, indent+1)}'
		s += f'\n	* count_2 = {fmt_member(self.count_2, indent+1)}'
		s += f'\n	* ptr_2 = {fmt_member(self.ptr_2, indent+1)}'
		s += f'\n	* num_xmls = {fmt_member(self.num_xmls, indent+1)}'
		s += f'\n	* ptr_xmls = {fmt_member(self.ptr_xmls, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
