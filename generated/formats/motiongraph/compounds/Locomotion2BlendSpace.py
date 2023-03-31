from generated.formats.base.basic import Uint64
from generated.formats.motiongraph.compounds.BlendSpaceAxis import BlendSpaceAxis
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Locomotion2BlendSpace(MemStruct):

	"""
	32 bytes
	"""

	__name__ = 'Locomotion2BlendSpace'

	_import_key = 'motiongraph.compounds.Locomotion2BlendSpace'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.y_axis = BlendSpaceAxis(self.context, 0, None)
		self.x_axis = BlendSpaceAxis(self.context, 0, None)
		self.nodes_count = 0
		self.nodes = ArrayPointer(self.context, self.nodes_count, Locomotion2BlendSpace._import_map["motiongraph.compounds.Locomotion2BlendSpaceNode"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('y_axis', BlendSpaceAxis, (0, None), (False, None), (None, None))
		yield ('x_axis', BlendSpaceAxis, (0, None), (False, None), (None, None))
		yield ('nodes_count', Uint64, (0, None), (False, None), (None, None))
		yield ('nodes', ArrayPointer, (None, Locomotion2BlendSpace._import_map["motiongraph.compounds.Locomotion2BlendSpaceNode"]), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'y_axis', BlendSpaceAxis, (0, None), (False, None)
		yield 'x_axis', BlendSpaceAxis, (0, None), (False, None)
		yield 'nodes_count', Uint64, (0, None), (False, None)
		yield 'nodes', ArrayPointer, (instance.nodes_count, Locomotion2BlendSpace._import_map["motiongraph.compounds.Locomotion2BlendSpaceNode"]), (False, None)


Locomotion2BlendSpace.init_attributes()
