from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ushort


class Vector3Ushort(BaseStruct):

	"""
	A signed int16 vector in 3D space (x,y,z).
	"""

	__name__ = 'Vector3Ushort'

	_import_key = 'bani.compounds.Vector3Ushort'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# First coordinate.
		self.x = 0

		# Second coordinate.
		self.y = 0

		# Third coordinate.
		self.z = 0
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('x', Ushort, (0, None), (False, None), None),
		('y', Ushort, (0, None), (False, None), None),
		('z', Ushort, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'x', Ushort, (0, None), (False, None)
		yield 'y', Ushort, (0, None), (False, None)
		yield 'z', Ushort, (0, None), (False, None)
