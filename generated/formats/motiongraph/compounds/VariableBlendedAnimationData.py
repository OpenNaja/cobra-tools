from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.motiongraph.compounds.DataStreamResourceDataList import DataStreamResourceDataList
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class VariableBlendedAnimationData(MemStruct):

	"""
	? bytes
	"""

	__name__ = 'VariableBlendedAnimationData'

	_import_key = 'motiongraph.compounds.VariableBlendedAnimationData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.value = 0.0
		self._pad = 0
		self.additional_data_streams = DataStreamResourceDataList(self.context, 0, None)
		self.animation = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('animation', Pointer, (0, ZString), (False, None), None),
		('value', Float, (0, None), (False, 0.0), None),
		('_pad', Uint, (0, None), (False, None), None),
		('additional_data_streams', DataStreamResourceDataList, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'animation', Pointer, (0, ZString), (False, None)
		yield 'value', Float, (0, None), (False, 0.0)
		yield '_pad', Uint, (0, None), (False, None)
		yield 'additional_data_streams', DataStreamResourceDataList, (0, None), (False, None)
