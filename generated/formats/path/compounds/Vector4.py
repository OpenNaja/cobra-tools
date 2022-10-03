from generated.formats.base.basic import Float
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Vector4(MemStruct):

	"""
	A vector in 3D space (x,y,z).
	"""

	__name__ = 'Vector4'

	_import_key = 'path.compounds.Vector4'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# First coordinate.
		self.x = 0.0

		# Second coordinate.
		self.y = 0.0

		# Third coordinate.
		self.z = 0.0

		# Fourth coordinate.
		self.w = 0.0
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('x', Float, (0, None), (False, None), None),
		('y', Float, (0, None), (False, None), None),
		('z', Float, (0, None), (False, None), None),
		('w', Float, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'x', Float, (0, None), (False, None)
		yield 'y', Float, (0, None), (False, None)
		yield 'z', Float, (0, None), (False, None)
		yield 'w', Float, (0, None), (False, None)
