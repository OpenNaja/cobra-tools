from generated.formats.base.basic import Float
from generated.formats.habitatboundary.structs.HbPhysicsOffsets import HbPhysicsOffsets
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class HbOffsets(MemStruct):

	__name__ = 'HB_Offsets'

	_import_key = 'habitatboundary.structs.HbOffsets'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.physics = HbPhysicsOffsets(self.context, 0, None)

		# Vertical offset of visible post above wall. Post height = wall_height + post_height_offset.
		self.post_height_offset = 0.0

		# The starting height of the barrier wall.
		self.wall_height = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('physics', HbPhysicsOffsets, (0, None), (False, None), None)
		yield ('post_height_offset', Float, (0, None), (False, None), None)
		yield ('wall_height', Float, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'physics', HbPhysicsOffsets, (0, None), (False, None)
		yield 'post_height_offset', Float, (0, None), (False, None)
		yield 'wall_height', Float, (0, None), (False, None)


HbOffsets.init_attributes()
