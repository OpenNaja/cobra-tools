from generated.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.renderparameters.compound.CurveList
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class CurveParam(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.dtype = 0

		# set to 1 if count > 1
		self.do_interpolation = 0
		self.count = 0
		self.attribute_name = 0
		self.curve_entries = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.dtype = 0
		self.do_interpolation = 0
		self.count = 0
		self.attribute_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.curve_entries = Pointer(self.context, self.count, generated.formats.renderparameters.compound.CurveList.CurveList)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.attribute_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.dtype = stream.read_int()
		instance.do_interpolation = stream.read_uint()
		instance.curve_entries = Pointer.from_stream(stream, instance.context, instance.count, generated.formats.renderparameters.compound.CurveList.CurveList)
		instance.count = stream.read_uint64()
		instance.attribute_name.arg = 0
		instance.curve_entries.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.attribute_name)
		stream.write_int(instance.dtype)
		stream.write_uint(instance.do_interpolation)
		Pointer.to_stream(stream, instance.curve_entries)
		stream.write_uint64(instance.count)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('attribute_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('dtype', Int, (0, None))
		yield ('do_interpolation', Uint, (0, None))
		yield ('curve_entries', Pointer, (instance.count, generated.formats.renderparameters.compound.CurveList.CurveList))
		yield ('count', Uint64, (0, None))

	def get_info_str(self, indent=0):
		return f'CurveParam [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* attribute_name = {fmt_member(self.attribute_name, indent+1)}'
		s += f'\n	* dtype = {fmt_member(self.dtype, indent+1)}'
		s += f'\n	* do_interpolation = {fmt_member(self.do_interpolation, indent+1)}'
		s += f'\n	* curve_entries = {fmt_member(self.curve_entries, indent+1)}'
		s += f'\n	* count = {fmt_member(self.count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
