from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.motiongraph.compounds.DataStreamResourceDataList import DataStreamResourceDataList
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class CoordinatedAnimationActivityData(MemStruct):

	"""
	72 bytes
	"""

	__name__ = 'CoordinatedAnimationActivityData'

	_import_key = 'motiongraph.compounds.CoordinatedAnimationActivityData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.waiting_anim_data_streams = DataStreamResourceDataList(self.context, 0, None)
		self.coordinated_anim_data_streams = DataStreamResourceDataList(self.context, 0, None)
		self.priorities = 0
		self.looping = 0
		self._pad = 0
		self.blend_time = 0.0
		self.coord_group = Pointer(self.context, 0, ZString)
		self.waiting_anim = Pointer(self.context, 0, ZString)
		self.coordinated_anim = Pointer(self.context, 0, ZString)
		self.output_prop_through_variable = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'coord_group', Pointer, (0, ZString), (False, None)
		yield 'waiting_anim', Pointer, (0, ZString), (False, None)
		yield 'waiting_anim_data_streams', DataStreamResourceDataList, (0, None), (False, None)
		yield 'coordinated_anim', Pointer, (0, ZString), (False, None)
		yield 'coordinated_anim_data_streams', DataStreamResourceDataList, (0, None), (False, None)
		yield 'priorities', Ubyte, (0, None), (False, None)
		yield 'looping', Ubyte, (0, None), (False, None)
		yield '_pad', Ushort, (0, None), (False, None)
		yield 'blend_time', Float, (0, None), (False, None)
		yield 'output_prop_through_variable', Pointer, (0, ZString), (False, None)
