import typing
from generated.formats.fgm.compound.Color import Color


class TextureInfo:

	"""
	part of fgm fragment, per texture involved
	"""

	# byte offset to name in fgm buffer
	offset: int

	# 7=has 2 8=uses texture indices
	is_textured: int

	# stores index into shader and array index of texture
	indices: typing.List[int]

	# Stores (usually) 2 rgba colors
	colors: typing.List[Color]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.offset = 0
		self.is_textured = 0
		self.indices = []
		self.colors = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.offset = stream.read_uint()
		self.is_textured = stream.read_uint()
		if self.is_textured == 8:
			self.indices = [stream.read_uint() for _ in range(4)]
		if self.is_textured == 7:
			self.colors = [stream.read_type(Color) for _ in range(4)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.offset)
		stream.write_uint(self.is_textured)
		if self.is_textured == 8:
			for item in self.indices: stream.write_uint(item)
		if self.is_textured == 7:
			for item in self.colors: stream.write_type(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'TextureInfo [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* offset = ' + self.offset.__repr__()
		s += '\n	* is_textured = ' + self.is_textured.__repr__()
		s += '\n	* indices = ' + self.indices.__repr__()
		s += '\n	* colors = ' + self.colors.__repr__()
		s += '\n'
		return s
