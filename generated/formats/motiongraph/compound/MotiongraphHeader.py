from source.formats.base.basic import fmt_member
from generated.context import ContextReference
from generated.formats.motiongraph.compound.Pointer import Pointer


class MotiongraphHeader:

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
		self.ptr_0 = Pointer(self.context, 0, None)
		self.ptr_1 = Pointer(self.context, 0, None)
		self.ptr_2 = Pointer(self.context, 0, None)
		self.ptr_3 = Pointer(self.context, 0, None)
		self.ptr_4 = Pointer(self.context, 0, None)
		self.ptr_5 = Pointer(self.context, 0, None)
		self.ptr_6 = Pointer(self.context, 0, None)
		self.ptr_7 = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.count_0 = 0
		self.count_1 = 0
		self.ptr_0 = Pointer(self.context, 0, None)
		self.ptr_1 = Pointer(self.context, 0, None)
		self.ptr_2 = Pointer(self.context, 0, None)
		self.ptr_3 = Pointer(self.context, 0, None)
		self.ptr_4 = Pointer(self.context, 0, None)
		self.ptr_5 = Pointer(self.context, 0, None)
		self.ptr_6 = Pointer(self.context, 0, None)
		self.ptr_7 = Pointer(self.context, 0, None)

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
		instance.ptr_0 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_1 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_2 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_3 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.count_0 = stream.read_uint()
		instance.count_1 = stream.read_uint()
		instance.ptr_4 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_5 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_6 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_7 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_0.arg = 0
		instance.ptr_1.arg = 0
		instance.ptr_2.arg = 0
		instance.ptr_3.arg = 0
		instance.ptr_4.arg = 0
		instance.ptr_5.arg = 0
		instance.ptr_6.arg = 0
		instance.ptr_7.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		Pointer.to_stream(stream, instance.ptr_0)
		Pointer.to_stream(stream, instance.ptr_1)
		Pointer.to_stream(stream, instance.ptr_2)
		Pointer.to_stream(stream, instance.ptr_3)
		stream.write_uint(instance.count_0)
		stream.write_uint(instance.count_1)
		Pointer.to_stream(stream, instance.ptr_4)
		Pointer.to_stream(stream, instance.ptr_5)
		Pointer.to_stream(stream, instance.ptr_6)
		Pointer.to_stream(stream, instance.ptr_7)

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
		return f'MotiongraphHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* ptr_0 = {fmt_member(self.ptr_0, indent+1)}'
		s += f'\n	* ptr_1 = {fmt_member(self.ptr_1, indent+1)}'
		s += f'\n	* ptr_2 = {fmt_member(self.ptr_2, indent+1)}'
		s += f'\n	* ptr_3 = {fmt_member(self.ptr_3, indent+1)}'
		s += f'\n	* count_0 = {fmt_member(self.count_0, indent+1)}'
		s += f'\n	* count_1 = {fmt_member(self.count_1, indent+1)}'
		s += f'\n	* ptr_4 = {fmt_member(self.ptr_4, indent+1)}'
		s += f'\n	* ptr_5 = {fmt_member(self.ptr_5, indent+1)}'
		s += f'\n	* ptr_6 = {fmt_member(self.ptr_6, indent+1)}'
		s += f'\n	* ptr_7 = {fmt_member(self.ptr_7, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
