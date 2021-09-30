import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.Matrix33 import Matrix33
from generated.formats.ms2.compound.Vector3 import Vector3


class ConvexHull:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 16 for anubis: 4 hulls * 16 * 12 (size of vert)
		self.vertex_count = 0
		self.rotation = Matrix33(context, None, None)

		# center of the box
		self.offset = Vector3(context, None, None)

		# probably padding
		if self.context.version == 18:
			self.zeros = numpy.zeros((5), dtype='uint')

		# probably padding
		if ((self.context.user_version == 8340) or (self.context.user_version == 8724)) and (self.context.version >= 19):
			self.zeros = numpy.zeros((2), dtype='uint')

	def read(self, stream):

		self.io_start = stream.tell()
		self.vertex_count = stream.read_uint()
		self.rotation = stream.read_type(Matrix33, (self.context, None, None))
		self.offset = stream.read_type(Vector3, (self.context, None, None))
		if self.context.version == 18:
			self.zeros = stream.read_uints((5))
		if ((self.context.user_version == 8340) or (self.context.user_version == 8724)) and (self.context.version >= 19):
			self.zeros = stream.read_uints((2))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.vertex_count)
		stream.write_type(self.rotation)
		stream.write_type(self.offset)
		if self.context.version == 18:
			stream.write_uints(self.zeros)
		if ((self.context.user_version == 8340) or (self.context.user_version == 8724)) and (self.context.version >= 19):
			stream.write_uints(self.zeros)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ConvexHull [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* vertex_count = {self.vertex_count.__repr__()}'
		s += f'\n	* rotation = {self.rotation.__repr__()}'
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
