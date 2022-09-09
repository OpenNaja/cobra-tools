from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.renderparameters.compounds.ParamData import ParamData
from generated.formats.renderparameters.enums.RenderParameterType import RenderParameterType


class Param(MemStruct):

	"""
	32 bytes
	"""

	__name__ = 'Param'

	_import_key = 'renderparameters.compounds.Param'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.dtype = RenderParameterType(self.context, 0, None)
		self.data = ParamData(self.context, self.dtype, None)
		self.attribute_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'attribute_name', Pointer, (0, ZString), (False, None)
		yield 'dtype', RenderParameterType, (0, None), (False, None)
		yield 'data', ParamData, (instance.dtype, None), (False, None)
