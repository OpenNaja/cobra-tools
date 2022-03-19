from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class RootFrag:

	"""
	first frag data
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.mat_type = 0
		self.ptr_0 = 0
		self.tex_count = 0
		self.ptr_1 = 0
		self.mat_count = 0
		self.ptr_2 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.mat_type = 0
		self.ptr_0 = 0
		self.tex_count = 0
		self.ptr_1 = 0
		self.mat_count = 0
		self.ptr_2 = 0

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
		instance.mat_type = stream.read_uint64()
		instance.ptr_0 = stream.read_uint64()
		instance.tex_count = stream.read_uint64()
		instance.ptr_1 = stream.read_uint64()
		instance.mat_count = stream.read_uint64()
		instance.ptr_2 = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint64(instance.mat_type)
		stream.write_uint64(instance.ptr_0)
		stream.write_uint64(instance.tex_count)
		stream.write_uint64(instance.ptr_1)
		stream.write_uint64(instance.mat_count)
		stream.write_uint64(instance.ptr_2)

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
		return f'RootFrag [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* mat_type = {fmt_member(self.mat_type, indent+1)}'
		s += f'\n	* ptr_0 = {fmt_member(self.ptr_0, indent+1)}'
		s += f'\n	* tex_count = {fmt_member(self.tex_count, indent+1)}'
		s += f'\n	* ptr_1 = {fmt_member(self.ptr_1, indent+1)}'
		s += f'\n	* mat_count = {fmt_member(self.mat_count, indent+1)}'
		s += f'\n	* ptr_2 = {fmt_member(self.ptr_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
