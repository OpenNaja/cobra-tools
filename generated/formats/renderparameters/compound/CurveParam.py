from source.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.renderparameters.compound.CurveList
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class CurveParam(MemStruct):

	"""
	#             # offset  x0: strz attribute name (Atmospherics.Lights.IrradianceScatterIntensity, ...)
	#             # offset  x8: int  type   (4294967296, 4294967297, 4294967303, 1...)
	#             # offset  xc: int unused (probably type is int64)
	#             # offset x10: list of ptr to curve entries
	#             # offset x18: count of curve entries
	#             # offset x1c: int unused (probably count is int64)
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.dtype = 0
		self.flag = 0
		self.count = 0
		self.attribute_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.curve_entries = Pointer(self.context, self.count, generated.formats.renderparameters.compound.CurveList.CurveList)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.dtype = 0
		self.flag = 0
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
		instance.flag = stream.read_uint()
		instance.curve_entries = Pointer.from_stream(stream, instance.context, instance.count, generated.formats.renderparameters.compound.CurveList.CurveList)
		instance.count = stream.read_uint64()
		instance.attribute_name.arg = 0
		instance.curve_entries.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.attribute_name)
		stream.write_int(instance.dtype)
		stream.write_uint(instance.flag)
		Pointer.to_stream(stream, instance.curve_entries)
		stream.write_uint64(instance.count)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'CurveParam [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* attribute_name = {fmt_member(self.attribute_name, indent+1)}'
		s += f'\n	* dtype = {fmt_member(self.dtype, indent+1)}'
		s += f'\n	* flag = {fmt_member(self.flag, indent+1)}'
		s += f'\n	* curve_entries = {fmt_member(self.curve_entries, indent+1)}'
		s += f'\n	* count = {fmt_member(self.count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
