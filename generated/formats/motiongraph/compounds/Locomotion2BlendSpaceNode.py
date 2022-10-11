from generated.formats.base.basic import Float
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Locomotion2BlendSpaceNode(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'Locomotion2BlendSpaceNode'

	_import_key = 'motiongraph.compounds.Locomotion2BlendSpaceNode'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.speed = 0.0
		self.orientation = 0.0
		self.anim_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('anim_name', Pointer, (0, ZString), (False, None), None),
		('speed', Float, (0, None), (False, None), None),
		('orientation', Float, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'anim_name', Pointer, (0, ZString), (False, None)
		yield 'speed', Float, (0, None), (False, None)
		yield 'orientation', Float, (0, None), (False, None)
