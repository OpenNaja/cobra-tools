import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Ushort


class UACJoint(BaseStruct):

	"""
	36 bytes
	"""

	__name__ = 'UACJoint'

	_import_path = 'generated.formats.ms2.compounds.UACJoint'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# variable
		self.unk = Array(self.context, 0, None, (0,), Ushort)

		# some at least
		self.floats = Array(self.context, 0, None, (0,), Float)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.unk = numpy.zeros((6,), dtype=numpy.dtype('uint16'))
		self.floats = numpy.zeros((6,), dtype=numpy.dtype('float32'))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk', Array, (0, None, (6,), Ushort), (False, None)
		yield 'floats', Array, (0, None, (6,), Float), (False, None)

	def get_info_str(self, indent=0):
		return f'UACJoint [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
