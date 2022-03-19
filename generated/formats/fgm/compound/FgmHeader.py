from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class FgmHeader:

	"""
	Sized str entry of 16 bytes, then ptrs, then padding
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.texture_count = 0
		self.texture_count = 0
		self.attribute_count = 0
		self.attribute_count = 0
		self.tex_ptr = 0
		self.attr_ptr = 0
		self.dependencies_ptr = 0
		self.data_ptr = 0
		self.unk_0 = 0
		self.unk_1 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if self.context.version <= 15:
			self.texture_count = 0
		if self.context.version >= 17:
			self.texture_count = 0
		if self.context.version <= 15:
			self.attribute_count = 0
		if self.context.version >= 17:
			self.attribute_count = 0
		self.tex_ptr = 0
		self.attr_ptr = 0
		self.dependencies_ptr = 0
		self.data_ptr = 0
		self.unk_0 = 0
		self.unk_1 = 0

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
		if instance.context.version <= 15:
			instance.texture_count = stream.read_uint()
		if instance.context.version >= 17:
			instance.texture_count = stream.read_uint64()
		if instance.context.version <= 15:
			instance.attribute_count = stream.read_uint()
		if instance.context.version >= 17:
			instance.attribute_count = stream.read_uint64()
		instance.tex_ptr = stream.read_uint64()
		instance.attr_ptr = stream.read_uint64()
		instance.dependencies_ptr = stream.read_uint64()
		instance.data_ptr = stream.read_uint64()
		instance.unk_0 = stream.read_uint64()
		instance.unk_1 = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		if instance.context.version <= 15:
			stream.write_uint(instance.texture_count)
		if instance.context.version >= 17:
			stream.write_uint64(instance.texture_count)
		if instance.context.version <= 15:
			stream.write_uint(instance.attribute_count)
		if instance.context.version >= 17:
			stream.write_uint64(instance.attribute_count)
		stream.write_uint64(instance.tex_ptr)
		stream.write_uint64(instance.attr_ptr)
		stream.write_uint64(instance.dependencies_ptr)
		stream.write_uint64(instance.data_ptr)
		stream.write_uint64(instance.unk_0)
		stream.write_uint64(instance.unk_1)

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
		return f'FgmHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* texture_count = {fmt_member(self.texture_count, indent+1)}'
		s += f'\n	* attribute_count = {fmt_member(self.attribute_count, indent+1)}'
		s += f'\n	* tex_ptr = {fmt_member(self.tex_ptr, indent+1)}'
		s += f'\n	* attr_ptr = {fmt_member(self.attr_ptr, indent+1)}'
		s += f'\n	* dependencies_ptr = {fmt_member(self.dependencies_ptr, indent+1)}'
		s += f'\n	* data_ptr = {fmt_member(self.data_ptr, indent+1)}'
		s += f'\n	* unk_0 = {fmt_member(self.unk_0, indent+1)}'
		s += f'\n	* unk_1 = {fmt_member(self.unk_1, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
