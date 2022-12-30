from generated.base_struct import BaseStruct
from generated.formats.base.basic import Normshort


class Vector4H(BaseStruct):

	"""
	A vector in 3D space (x,y,z).
	"""

	__name__ = 'Vector4H'

	_import_key = 'manis.compounds.Vector4H'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# First coordinate.
		self.x = 0

		# Second coordinate.
		self.y = 0

		# Third coordinate.
		self.z = 0

		# Fourth coordinate.
		self.w = 0
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('x', Normshort, (0, None), (False, None), None),
		('y', Normshort, (0, None), (False, None), None),
		('z', Normshort, (0, None), (False, None), None),
		('w', Normshort, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'x', Normshort, (0, None), (False, None)
		yield 'y', Normshort, (0, None), (False, None)
		yield 'z', Normshort, (0, None), (False, None)
		yield 'w', Normshort, (0, None), (False, None)
