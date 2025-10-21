from generated.array import Array
from generated.formats.ms2.imports import name_type_map
from generated.formats.ms2.structs.Matrix import Matrix


class Matrix44(Matrix):

	"""
	A 4x4 transformation matrix.
	"""

	__name__ = 'Matrix44'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Stored in OpenGL column-major format.
		self.data = Array(self.context, 0, None, (0,), name_type_map['Float'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'data', Array, (0, None, (4, 4,), name_type_map['Float']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'data', Array, (0, None, (4, 4,), name_type_map['Float']), (False, None)
