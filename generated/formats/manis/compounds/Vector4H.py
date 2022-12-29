import Hfloat
from generated.base_struct import BaseStruct


class Vector4H(BaseStruct):

	"""
	A vector in 3D space (x,y,z).
	"""

	__name__ = 'Vector4H'

	_import_key = 'manis.compounds.Vector4H'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# First coordinate.
		self.x = Hfloat(self.context, 0, None)

		# Second coordinate.
		self.y = Hfloat(self.context, 0, None)

		# Third coordinate.
		self.z = Hfloat(self.context, 0, None)

		# Fourth coordinate.
		self.w = Hfloat(self.context, 0, None)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('x', None, (0, None), (False, None), None),
		('y', None, (0, None), (False, None), None),
		('z', None, (0, None), (False, None), None),
		('w', None, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'x', Hfloat, (0, None), (False, None)
		yield 'y', Hfloat, (0, None), (False, None)
		yield 'z', Hfloat, (0, None), (False, None)
		yield 'w', Hfloat, (0, None), (False, None)
