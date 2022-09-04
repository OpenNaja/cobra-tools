from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.basic import ZStringObfuscated
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class RenderParameterCurvesRoot(MemStruct):

	"""
	32 bytes
	"""

	__name__ = 'RenderParameterCurvesRoot'

	_import_path = 'generated.formats.renderparameters.compounds.RenderParameterCurvesRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.unk = 0
		self.param_name = Pointer(self.context, 0, ZStringObfuscated)
		self.params = Pointer(self.context, self.count, RenderParameterCurvesRoot._import_path_map["generated.formats.renderparameters.compounds.CurveParamList"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count = 0
		self.unk = 0
		self.param_name = Pointer(self.context, 0, ZStringObfuscated)
		self.params = Pointer(self.context, self.count, RenderParameterCurvesRoot._import_path_map["generated.formats.renderparameters.compounds.CurveParamList"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.param_name = Pointer.from_stream(stream, instance.context, 0, ZStringObfuscated)
		instance.params = Pointer.from_stream(stream, instance.context, instance.count, RenderParameterCurvesRoot._import_path_map["generated.formats.renderparameters.compounds.CurveParamList"])
		instance.count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.unk = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.param_name, int):
			instance.param_name.arg = 0
		if not isinstance(instance.params, int):
			instance.params.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.param_name)
		Pointer.to_stream(stream, instance.params)
		Uint64.to_stream(stream, instance.count)
		Uint64.to_stream(stream, instance.unk)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'param_name', Pointer, (0, ZStringObfuscated), (False, None)
		yield 'params', Pointer, (instance.count, RenderParameterCurvesRoot._import_path_map["generated.formats.renderparameters.compounds.CurveParamList"]), (False, None)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'unk', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'RenderParameterCurvesRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
