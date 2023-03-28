from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.basic import ZStringObfuscated
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class RenderParameterCurvesRoot(MemStruct):

	"""
	32 bytes
	"""

	__name__ = 'RenderParameterCurvesRoot'

	_import_key = 'renderparameters.compounds.RenderParameterCurvesRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.unk = 0
		self.param_name = Pointer(self.context, 0, ZStringObfuscated)
		self.params = Pointer(self.context, self.count, RenderParameterCurvesRoot._import_map["renderparameters.compounds.CurveParamList"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('param_name', Pointer, (0, ZStringObfuscated), (False, None), (None, None))
		yield ('params', Pointer, (None, RenderParameterCurvesRoot._import_map["renderparameters.compounds.CurveParamList"]), (False, None), (None, None))
		yield ('count', Uint64, (0, None), (False, None), (None, None))
		yield ('unk', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'param_name', Pointer, (0, ZStringObfuscated), (False, None)
		yield 'params', Pointer, (instance.count, RenderParameterCurvesRoot._import_map["renderparameters.compounds.CurveParamList"]), (False, None)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'unk', Uint64, (0, None), (False, None)


RenderParameterCurvesRoot.init_attributes()
