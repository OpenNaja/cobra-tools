import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.ms2.compounds.Descriptor import Descriptor
from generated.formats.ms2.compounds.Vector3 import Vector3


class ListLong(Descriptor):

	"""
	probably ragdoll, lots of angles
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# the location of the child joint
		self.loc = Vector3(self.context, 0, None)

		# each of the vec3 components is normalized, these might represent axes for the angles
		self.floats = numpy.zeros((5, 3,), dtype=numpy.dtype('float32'))

		# radians
		self.radians = numpy.zeros((8,), dtype=numpy.dtype('float32'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.loc = Vector3(self.context, 0, None)
		self.floats = numpy.zeros((5, 3,), dtype=numpy.dtype('float32'))
		self.radians = numpy.zeros((8,), dtype=numpy.dtype('float32'))

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
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'loc', Vector3, (0, None)
		yield 'floats', Array, ((5, 3,), Float, 0, None)
		yield 'radians', Array, ((8,), Float, 0, None)

	def get_info_str(self, indent=0):
		return f'ListLong [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* loc = {self.fmt_member(self.loc, indent+1)}'
		s += f'\n	* floats = {self.fmt_member(self.floats, indent+1)}'
		s += f'\n	* radians = {self.fmt_member(self.radians, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
