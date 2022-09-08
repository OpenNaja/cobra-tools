import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.ms2.compounds.Descriptor import Descriptor
from generated.formats.ms2.compounds.Vector3 import Vector3


class ListLong(Descriptor):

	"""
	probably ragdoll, lots of angles
	"""

	__name__ = 'ListLong'

	_import_path = 'generated.formats.ms2.compounds.ListLong'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# the location of the child joint
		self.loc = Vector3(self.context, 0, None)

		# each of the vec3 components is normalized, these might represent axes for the angles
		self.floats = Array(self.context, 0, None, (0,), Float)

		# radians
		self.radians = Array(self.context, 0, None, (0,), Float)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.loc = Vector3(self.context, 0, None)
		self.floats = numpy.zeros((5, 3,), dtype=numpy.dtype('float32'))
		self.radians = numpy.zeros((8,), dtype=numpy.dtype('float32'))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'loc', Vector3, (0, None), (False, None)
		yield 'floats', Array, (0, None, (5, 3,), Float), (False, None)
		yield 'radians', Array, (0, None, (8,), Float), (False, None)

	def get_info_str(self, indent=0):
		return f'ListLong [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
