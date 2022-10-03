import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float


class Matrix44(BaseStruct):

	"""
	A 4x4 transformation matrix.
	"""

	__name__ = 'Matrix44'

	_import_key = 'ms2.compounds.Matrix44'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Stored in OpenGL column-major format.
		self.data = Array(self.context, 0, None, (0,), Float)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('data', Array, (0, None, (4, 4,), Float), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'data', Array, (0, None, (4, 4,), Float), (False, None)

	def set_rows(self, mat):
		"""Set matrix from rows."""
		self.data[:] = mat.transposed()

