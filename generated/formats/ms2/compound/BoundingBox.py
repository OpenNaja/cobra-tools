import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.Matrix33 import Matrix33
from generated.formats.ms2.compound.Vector3 import Vector3


class BoundingBox:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.rotation = Matrix33(self.context, None, None)

		# center of the box
		self.center = Vector3(self.context, None, None)

		# total width
		self.extent = Vector3(self.context, None, None)

		# probably padding
		self.zeros = numpy.zeros((3), dtype='uint')
		self.set_defaults()

	def set_defaults(self):
		self.rotation = Matrix33(self.context, None, None)
		self.center = Vector3(self.context, None, None)
		self.extent = Vector3(self.context, None, None)
		if self.context.version == 18:
			self.zeros = numpy.zeros((3), dtype='uint')

	def read(self, stream):
		self.io_start = stream.tell()
		self.rotation = stream.read_type(Matrix33, (self.context, None, None))
		self.center = stream.read_type(Vector3, (self.context, None, None))
		self.extent = stream.read_type(Vector3, (self.context, None, None))
		if self.context.version == 18:
			self.zeros = stream.read_uints((3))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.rotation)
		stream.write_type(self.center)
		stream.write_type(self.extent)
		if self.context.version == 18:
			stream.write_uints(self.zeros)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'BoundingBox [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* rotation = {self.rotation.__repr__()}'
		s += f'\n	* center = {self.center.__repr__()}'
		s += f'\n	* extent = {self.extent.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
