from generated.base_struct import BaseStruct
from generated.formats.base.imports import name_type_map


class Vector3Half(BaseStruct):

	"""
	A vector in 3D space (x,y,z).
	"""

	__name__ = 'Vector3Half'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# First coordinate.
		self.x = name_type_map['Hfloat'](self.context, 0, None)

		# Second coordinate.
		self.y = name_type_map['Hfloat'](self.context, 0, None)

		# Third coordinate.
		self.z = name_type_map['Hfloat'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'x', name_type_map['Hfloat'], (0, None), (False, None), (None, None)
		yield 'y', name_type_map['Hfloat'], (0, None), (False, None), (None, None)
		yield 'z', name_type_map['Hfloat'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'x', name_type_map['Hfloat'], (0, None), (False, None)
		yield 'y', name_type_map['Hfloat'], (0, None), (False, None)
		yield 'z', name_type_map['Hfloat'], (0, None), (False, None)
