from source.formats.base.basic import fmt_member
import numpy
from generated.formats.ms2.compound.Descriptor import Descriptor
from generated.formats.ms2.compound.Vector3 import Vector3


class ListLong(Descriptor):

	"""
	probably ragdoll, lots of angles
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# the location of the child joint
		self.loc = 0

		# each of the vec3 components is normalized, these might represent axes for the angles
		self.floats = 0

		# radians
		self.radians = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.loc = Vector3(self.context, 0, None)
		self.floats = numpy.zeros((5, 3,), dtype=numpy.dtype('float32'))
		self.radians = numpy.zeros((8,), dtype=numpy.dtype('float32'))

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
		instance.loc = Vector3.from_stream(stream, instance.context, 0, None)
		instance.floats = stream.read_floats((5, 3,))
		instance.radians = stream.read_floats((8,))

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Vector3.to_stream(stream, instance.loc)
		stream.write_floats(instance.floats)
		stream.write_floats(instance.radians)

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
		return f'ListLong [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* loc = {fmt_member(self.loc, indent+1)}'
		s += f'\n	* floats = {fmt_member(self.floats, indent+1)}'
		s += f'\n	* radians = {fmt_member(self.radians, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
