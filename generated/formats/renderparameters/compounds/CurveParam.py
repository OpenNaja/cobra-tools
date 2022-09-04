from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class CurveParam(MemStruct):

	__name__ = 'CurveParam'

	_import_path = 'generated.formats.renderparameters.compounds.CurveParam'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.dtype = 0

		# set to 1 if count > 1
		self.do_interpolation = 0
		self.count = 0
		self.attribute_name = Pointer(self.context, 0, ZString)
		self.curve_entries = Pointer(self.context, self.count, CurveParam._import_path_map["generated.formats.renderparameters.compounds.CurveList"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		# leaving self.dtype alone
		self.do_interpolation = 0
		self.count = 0
		self.attribute_name = Pointer(self.context, 0, ZString)
		self.curve_entries = Pointer(self.context, self.count, CurveParam._import_path_map["generated.formats.renderparameters.compounds.CurveList"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.attribute_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.dtype = Int.from_stream(stream, instance.context, 0, None)
		instance.do_interpolation = Uint.from_stream(stream, instance.context, 0, None)
		instance.curve_entries = Pointer.from_stream(stream, instance.context, instance.count, CurveParam._import_path_map["generated.formats.renderparameters.compounds.CurveList"])
		instance.count = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.attribute_name, int):
			instance.attribute_name.arg = 0
		if not isinstance(instance.curve_entries, int):
			instance.curve_entries.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.attribute_name)
		Int.to_stream(stream, instance.dtype)
		Uint.to_stream(stream, instance.do_interpolation)
		Pointer.to_stream(stream, instance.curve_entries)
		Uint64.to_stream(stream, instance.count)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'attribute_name', Pointer, (0, ZString), (False, None)
		yield 'dtype', Int, (0, None), (False, None)
		yield 'do_interpolation', Uint, (0, None), (False, None)
		yield 'curve_entries', Pointer, (instance.count, CurveParam._import_path_map["generated.formats.renderparameters.compounds.CurveList"]), (False, None)
		yield 'count', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'CurveParam [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
