import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float


class Matrix33(BaseStruct):

	"""
	A 3x3 rotation matrix; M^T M=identity, det(M)=1.
	"""

	__name__ = 'Matrix33'

	_import_path = 'generated.formats.ms2.compounds.Matrix33'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Stored in OpenGL column-major format.
		self.data = Array(self.context, 0, None, (0,), Float)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.data = numpy.zeros((3, 3,), dtype=numpy.dtype('float32'))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'data', Array, (0, None, (3, 3,), Float), (False, None)

	def get_info_str(self, indent=0):
		return f'Matrix33 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
