from generated.array import Array
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class CurveParamList(MemStruct):

	"""
	this is not null ptr terminated, but padded to 16 bytes at the end
	"""

	__name__ = 'CurveParamList'

	_import_path = 'generated.formats.renderparameters.compounds.CurveParamList'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ptrs = Array(self.context, 0, CurveParamList._import_path_map["generated.formats.renderparameters.compounds.CurveParam"], (0,), Pointer)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.ptrs = Array(self.context, 0, CurveParamList._import_path_map["generated.formats.renderparameters.compounds.CurveParam"], (self.arg,), Pointer)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.ptrs = Array.from_stream(stream, instance.context, 0, CurveParamList._import_path_map["generated.formats.renderparameters.compounds.CurveParam"], (instance.arg,), Pointer)
		if not isinstance(instance.ptrs, int):
			instance.ptrs.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.ptrs, instance.context, 0, CurveParamList._import_path_map["generated.formats.renderparameters.compounds.CurveParam"], (instance.arg,), Pointer)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'ptrs', Array, (0, CurveParamList._import_path_map["generated.formats.renderparameters.compounds.CurveParam"], (instance.arg,), Pointer), (False, None)

	def get_info_str(self, indent=0):
		return f'CurveParamList [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
