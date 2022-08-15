import generated.formats.ovl_base.basic
import generated.formats.renderparameters.compounds.ParamList
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class RenderParametersRoot(MemStruct):

	"""
	32 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.unk = 0
		self.param_name = Pointer(self.context, 0, generated.formats.ovl_base.basic.ZStringObfuscated)
		self.params = Pointer(self.context, self.count, generated.formats.renderparameters.compounds.ParamList.ParamList)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count = 0
		self.unk = 0
		self.param_name = Pointer(self.context, 0, generated.formats.ovl_base.basic.ZStringObfuscated)
		self.params = Pointer(self.context, self.count, generated.formats.renderparameters.compounds.ParamList.ParamList)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.param_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.ovl_base.basic.ZStringObfuscated)
		instance.params = Pointer.from_stream(stream, instance.context, instance.count, generated.formats.renderparameters.compounds.ParamList.ParamList)
		instance.count = stream.read_uint64()
		instance.unk = stream.read_uint64()
		if not isinstance(instance.param_name, int):
			instance.param_name.arg = 0
		if not isinstance(instance.params, int):
			instance.params.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.param_name)
		Pointer.to_stream(stream, instance.params)
		stream.write_uint64(instance.count)
		stream.write_uint64(instance.unk)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'param_name', Pointer, (0, generated.formats.ovl_base.basic.ZStringObfuscated)
		yield 'params', Pointer, (instance.count, generated.formats.renderparameters.compounds.ParamList.ParamList)
		yield 'count', Uint64, (0, None)
		yield 'unk', Uint64, (0, None)

	def get_info_str(self, indent=0):
		return f'RenderParametersRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* param_name = {self.fmt_member(self.param_name, indent+1)}'
		s += f'\n	* params = {self.fmt_member(self.params, indent+1)}'
		s += f'\n	* count = {self.fmt_member(self.count, indent+1)}'
		s += f'\n	* unk = {self.fmt_member(self.unk, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
