import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.fgm.compound.Color import Color


class TextureInfo:

	"""
	part of fgm fragment, per texture involved
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
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
		self.indices = numpy.zeros((4), dtype=numpy.dtype('uint32'))

		# Stores (usually) 2 rgba colors
		self.colors = Array((4), Color, self.context, None, None)

		# stores index into shader
		self.indices = numpy.zeros((1), dtype=numpy.dtype('uint32'))

		# Stores rgba color
		self.colors = Array((1), Color, self.context, None, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.offset = 0
		self.is_textured = 0
		if not (self.context.version == 17) and self.is_textured == 8:
			self.indices = numpy.zeros((4), dtype=numpy.dtype('uint32'))
		if not (self.context.version == 17) and self.is_textured == 7:
			self.colors = Array((4), Color, self.context, None, None)
		if self.context.version == 17 and self.is_textured == 8:
			self.indices = numpy.zeros((1), dtype=numpy.dtype('uint32'))
		if self.context.version == 17 and self.is_textured == 7:
			self.colors = Array((1), Color, self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.offset = stream.read_uint()
		self.is_textured = stream.read_uint()
		if not (self.context.version == 17) and self.is_textured == 8:
			self.indices = stream.read_uints((4))
		if not (self.context.version == 17) and self.is_textured == 7:
			self.colors.read(stream, Color, 4, None)
		if self.context.version == 17 and self.is_textured == 8:
			self.indices = stream.read_uints((1))
		if self.context.version == 17 and self.is_textured == 7:
			self.colors.read(stream, Color, 1, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.offset)
		stream.write_uint(self.is_textured)
		if not (self.context.version == 17) and self.is_textured == 8:
			stream.write_uints(self.indices)
		if not (self.context.version == 17) and self.is_textured == 7:
			self.colors.write(stream, Color, 4, None)
		if self.context.version == 17 and self.is_textured == 8:
			stream.write_uints(self.indices)
		if self.context.version == 17 and self.is_textured == 7:
			self.colors.write(stream, Color, 1, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'TextureInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* is_textured = {self.is_textured.__repr__()}'
		s += f'\n	* indices = {self.indices.__repr__()}'
		s += f'\n	* colors = {self.colors.__repr__()}'
		s += f'\n	* indices = {self.indices.__repr__()}'
		s += f'\n	* colors = {self.colors.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
