import numpy
from generated.array import Array
from generated.formats.ms2.compound.Descriptor import Descriptor
from generated.formats.ms2.compound.Vector3 import Vector3


class ListLong(Descriptor):

	"""
	probably ragdoll, lots of angles
	"""

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# the location of the child joint
		self.loc = Vector3(self.context, None, None)

		# each of the vec3 components is normalized, these might represent axes for the angles
		self.floats = numpy.zeros((5, 3), dtype='float')

		# radians
		self.radians = numpy.zeros((8), dtype='float')
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.loc = Vector3(self.context, None, None)
		self.floats = numpy.zeros((5, 3), dtype='float')
		self.radians = numpy.zeros((8), dtype='float')

	def read(self, stream):
		self.io_start = stream.tell()
		super().read(stream)
		self.loc = stream.read_type(Vector3, (self.context, None, None))
		self.floats = stream.read_floats((5, 3))
		self.radians = stream.read_floats((8))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		super().write(stream)
		stream.write_type(self.loc)
		stream.write_floats(self.floats)
		stream.write_floats(self.radians)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ListLong [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* loc = {self.loc.__repr__()}'
		s += f'\n	* floats = {self.floats.__repr__()}'
		s += f'\n	* radians = {self.radians.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
