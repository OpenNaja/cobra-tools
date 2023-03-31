from generated.formats.base.basic import Float
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class HbDoorCutout(MemStruct):

	"""
	Positions to create door cutout in a wall.
	"""

	__name__ = 'HB_DoorCutout'

	_import_key = 'habitatboundary.structs.HbDoorCutout'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Wall cutout height for door.
		self.height = 0.0

		# Wall cutout position for right of door.
		self.right = 0.0

		# Wall cutout position for left of door.
		self.left = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('height', Float, (0, None), (False, None), (None, None))
		yield ('right', Float, (0, None), (False, None), (None, None))
		yield ('left', Float, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'height', Float, (0, None), (False, None)
		yield 'right', Float, (0, None), (False, None)
		yield 'left', Float, (0, None), (False, None)


HbDoorCutout.init_attributes()
