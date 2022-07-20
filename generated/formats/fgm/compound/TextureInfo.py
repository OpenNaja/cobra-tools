from source.formats.base.basic import fmt_member
from generated.array import Array
from generated.formats.fgm.compound.Color import Color
from generated.formats.fgm.compound.GenericInfo import GenericInfo
from generated.formats.fgm.compound.TexIndex import TexIndex


class TextureInfo(GenericInfo):

	"""
	part of fgm fragment, per texture involved
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.value = 0

		# Stores 2 rgba colors
		self.value = 0

		# Stores rgba color
		self.value = 0
		self.some_index_0 = 0
		self.some_index_1 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if self.dtype == 8:
			self.value = Array((1,), TexIndex, self.context, 0, None)
		if self.context.version >= 18 and self.dtype == 7:
			self.value = Array((2,), Color, self.context, 0, None)
		if self.context.version <= 17 and self.dtype == 7:
			self.value = Array((1,), Color, self.context, 0, None)
		if self.context.version >= 18:
			self.some_index_0 = 0
		if self.context.version >= 18:
			self.some_index_1 = 0

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
		super().read_fields(stream, instance)
		if instance.dtype == 8:
			instance.value = Array.from_stream(stream, (1,), TexIndex, instance.context, 0, None)
		if instance.context.version >= 18 and instance.dtype == 7:
			instance.value = Array.from_stream(stream, (2,), Color, instance.context, 0, None)
		if instance.context.version <= 17 and instance.dtype == 7:
			instance.value = Array.from_stream(stream, (1,), Color, instance.context, 0, None)
		if instance.context.version >= 18:
			instance.some_index_0 = stream.read_uint()
			instance.some_index_1 = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.dtype == 8:
			Array.to_stream(stream, instance.value, (1,), TexIndex, instance.context, 0, None)
		if instance.context.version >= 18 and instance.dtype == 7:
			Array.to_stream(stream, instance.value, (2,), Color, instance.context, 0, None)
		if instance.context.version <= 17 and instance.dtype == 7:
			Array.to_stream(stream, instance.value, (1,), Color, instance.context, 0, None)
		if instance.context.version >= 18:
			stream.write_uint(instance.some_index_0)
			stream.write_uint(instance.some_index_1)

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
		return f'TextureInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* value = {fmt_member(self.value, indent+1)}'
		s += f'\n	* some_index_0 = {fmt_member(self.some_index_0, indent+1)}'
		s += f'\n	* some_index_1 = {fmt_member(self.some_index_1, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
