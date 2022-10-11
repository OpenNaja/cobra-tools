from generated.formats.base.basic import Float
from generated.formats.habitatboundary.structs.HbPostSize import HbPostSize
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class HbPhysicsOffsets(MemStruct):

	"""
	Physics values for barriers.
	"""

	__name__ = 'HB_PhysicsOffsets'

	_import_key = 'habitatboundary.structs.HbPhysicsOffsets'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Wall thickness. Affects navcut, selection, and climb nav width. Must be under a certain value or it crashes.
		self.thickness = 0.0
		self.post_size = HbPostSize(self.context, 0, None)

		# Wall size above wall_height. Affects navcut, selection, and climb nav height.
		self.wall_pad_top = 0.0

		# Distance between post center and start of wall. Larger values create a visual and nav gap between the post and wall segment.
		self.wall_post_gap = 0.0
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('thickness', Float, (0, None), (False, None), None),
		('post_size', HbPostSize, (0, None), (False, None), None),
		('wall_pad_top', Float, (0, None), (False, None), None),
		('wall_post_gap', Float, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'thickness', Float, (0, None), (False, None)
		yield 'post_size', HbPostSize, (0, None), (False, None)
		yield 'wall_pad_top', Float, (0, None), (False, None)
		yield 'wall_post_gap', Float, (0, None), (False, None)
