from source.formats.base.basic import fmt_member
import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.fgm.compound.Color import Color


class TextureInfo:

	"""
	part of fgm fragment, per texture involved
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# byte offset to name in fgm buffer
		self.offset = 0

		# 7=has RGB 8=uses texture indices
		self.is_textured = 0

		# stores index into shader and array index of texture
		self.indices = numpy.zeros((4,), dtype=numpy.dtype('uint32'))

		# Stores (usually) 2 rgba colors
		self.colors = Array((4,), Color, self.context, 0, None)

		# stores index into shader
		self.indices = numpy.zeros((1,), dtype=numpy.dtype('uint32'))

		# Stores rgba color
		self.colors = Array((1,), Color, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.offset = 0
		self.is_textured = 0
		if not (self.context.version == 17) and self.is_textured == 8:
			self.indices = numpy.zeros((4,), dtype=numpy.dtype('uint32'))
		if not (self.context.version == 17) and self.is_textured == 7:
			self.colors = Array((4,), Color, self.context, 0, None)
		if self.context.version == 17 and self.is_textured == 8:
			self.indices = numpy.zeros((1,), dtype=numpy.dtype('uint32'))
		if self.context.version == 17 and self.is_textured == 7:
			self.colors = Array((1,), Color, self.context, 0, None)

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
		instance.offset = stream.read_uint()
		instance.is_textured = stream.read_uint()
		if not (instance.context.version == 17) and instance.is_textured == 8:
			instance.indices = stream.read_uints((4,))
		if not (instance.context.version == 17) and instance.is_textured == 7:
			instance.colors = Array.from_stream(stream, (4,), Color, instance.context, 0, None)
		if instance.context.version == 17 and instance.is_textured == 8:
			instance.indices = stream.read_uints((1,))
		if instance.context.version == 17 and instance.is_textured == 7:
			instance.colors = Array.from_stream(stream, (1,), Color, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.offset)
		stream.write_uint(instance.is_textured)
		if not (instance.context.version == 17) and instance.is_textured == 8:
			stream.write_uints(instance.indices)
		if not (instance.context.version == 17) and instance.is_textured == 7:
			Array.to_stream(stream, instance.colors, (4,), Color, instance.context, 0, None)
		if instance.context.version == 17 and instance.is_textured == 8:
			stream.write_uints(instance.indices)
		if instance.context.version == 17 and instance.is_textured == 7:
			Array.to_stream(stream, instance.colors, (1,), Color, instance.context, 0, None)

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
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* is_textured = {fmt_member(self.is_textured, indent+1)}'
		s += f'\n	* indices = {fmt_member(self.indices, indent+1)}'
		s += f'\n	* colors = {fmt_member(self.colors, indent+1)}'
		s += f'\n	* indices = {fmt_member(self.indices, indent+1)}'
		s += f'\n	* colors = {fmt_member(self.colors, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
