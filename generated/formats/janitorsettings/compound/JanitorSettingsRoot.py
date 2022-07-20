from source.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.janitorsettings.compound.UIntPair
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class JanitorSettingsRoot(MemStruct):

	"""
	huge batch of arrays at the head of the file
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.unk_0 = 0
		self.unk_1 = 0
		self.unk_2 = 0
		self.unk_3 = 0
		self.unk_4 = 0
		self.unk_5 = 0
		self.unk_6 = 0
		self.unk_7 = 0
		self.unk_8 = 0
		self.unk_9 = 0
		self.unk_10 = 0
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.count_3 = 0
		self.count_4 = 0
		self.count_5 = 0
		self.count_6 = 0
		self.count_7 = 0
		self.count_8 = 0
		self.count_9 = 0
		self.count_10 = 0
		self.count_11 = 0
		self.count_12 = 0
		self.count_13 = 0
		self.count_14 = 0
		self.possibly_unused_count_0 = 0
		self.possibly_unused_count_1 = 0
		self.possibly_unused_count_2 = 0
		self.possibly_unused_count_3 = 0
		self.possibly_unused_count_4 = 0
		self.unk_11 = 0
		self.unk_12 = 0
		self.unk_13 = 0
		self.unk_14 = 0
		self.unk_15 = 0
		self.unk_16 = 0
		self.unk_17 = 0
		self.unk_18 = 0
		self.unk_19 = 0
		self.unk_20 = 0
		self.unk_21 = 0
		self.unk_22 = 0
		self.unk_23 = 0
		self.unk_24 = 0
		self.unk_25 = 0
		self.unk_26 = 0
		self.unk_27 = 0
		self.unk_28 = 0
		self.unk_29 = 0
		self.unk_30 = 0
		self.unk_31 = 0
		self.unk_32 = 0
		self.array_0 = 0
		self.array_1 = 0
		self.array_2 = 0
		self.array_3 = 0
		self.array_4 = 0
		self.array_5 = 0
		self.array_6 = 0
		self.array_7 = 0
		self.array_8 = 0
		self.array_9 = 0
		self.array_10 = 0
		self.array_11 = 0
		self.array_12 = 0
		self.array_13 = 0
		self.array_14 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.unk_0 = 0.0
		self.unk_1 = 0.0
		self.unk_2 = 0.0
		self.unk_3 = 0.0
		self.unk_4 = 0.0
		self.unk_5 = 0.0
		self.unk_6 = 0.0
		self.unk_7 = 0.0
		self.unk_8 = 0
		self.unk_9 = 0.0
		self.unk_10 = 0.0
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.count_3 = 0
		self.count_4 = 0
		self.count_5 = 0
		self.count_6 = 0
		self.count_7 = 0
		self.count_8 = 0
		self.count_9 = 0
		self.count_10 = 0
		self.count_11 = 0
		self.count_12 = 0
		self.count_13 = 0
		self.count_14 = 0
		self.possibly_unused_count_0 = 0
		self.possibly_unused_count_1 = 0
		self.possibly_unused_count_2 = 0
		self.possibly_unused_count_3 = 0
		self.possibly_unused_count_4 = 0
		self.unk_11 = 0.0
		self.unk_12 = 0.0
		self.unk_13 = 0.0
		self.unk_14 = 0.0
		self.unk_15 = 0.0
		self.unk_16 = 0.0
		self.unk_17 = 0.0
		self.unk_18 = 0.0
		self.unk_19 = 0.0
		self.unk_20 = 0.0
		self.unk_21 = 0.0
		self.unk_22 = 0.0
		self.unk_23 = 0.0
		self.unk_24 = 0.0
		self.unk_25 = 0.0
		self.unk_26 = 0.0
		self.unk_27 = 0.0
		self.unk_28 = 0.0
		self.unk_29 = 0.0
		self.unk_30 = 0.0
		self.unk_31 = 0.0
		self.unk_32 = 0.0
		self.array_0 = ArrayPointer(self.context, self.count_0, generated.formats.janitorsettings.compound.UIntPair.UIntPair)
		self.array_1 = ArrayPointer(self.context, self.count_1, generated.formats.janitorsettings.compound.UIntPair.UIntPair)
		self.array_2 = ArrayPointer(self.context, self.count_2, generated.formats.janitorsettings.compound.UIntPair.UIntPair)
		self.array_3 = ArrayPointer(self.context, self.count_3, generated.formats.janitorsettings.compound.UIntPair.UIntPair)
		self.array_4 = ArrayPointer(self.context, self.count_4, generated.formats.janitorsettings.compound.UIntPair.UIntPair)
		self.array_5 = ArrayPointer(self.context, self.count_5, generated.formats.janitorsettings.compound.UIntPair.UIntPair)
		self.array_6 = ArrayPointer(self.context, self.count_6, generated.formats.base.basic.Uint)
		self.array_7 = ArrayPointer(self.context, self.count_7, generated.formats.base.basic.Uint)
		self.array_8 = ArrayPointer(self.context, self.count_8, generated.formats.base.basic.Uint)
		self.array_9 = ArrayPointer(self.context, self.count_9, generated.formats.base.basic.Float)
		self.array_10 = ArrayPointer(self.context, self.count_10, generated.formats.base.basic.Float)
		self.array_11 = ArrayPointer(self.context, self.count_11, generated.formats.base.basic.Float)
		self.array_12 = ArrayPointer(self.context, self.count_12, generated.formats.base.basic.Float)
		self.array_13 = ArrayPointer(self.context, self.count_13, generated.formats.base.basic.Float)
		self.array_14 = ArrayPointer(self.context, self.count_14, generated.formats.base.basic.Float)

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
		instance.array_0 = ArrayPointer.from_stream(stream, instance.context, instance.count_0, generated.formats.janitorsettings.compound.UIntPair.UIntPair)
		instance.array_1 = ArrayPointer.from_stream(stream, instance.context, instance.count_1, generated.formats.janitorsettings.compound.UIntPair.UIntPair)
		instance.array_2 = ArrayPointer.from_stream(stream, instance.context, instance.count_2, generated.formats.janitorsettings.compound.UIntPair.UIntPair)
		instance.array_3 = ArrayPointer.from_stream(stream, instance.context, instance.count_3, generated.formats.janitorsettings.compound.UIntPair.UIntPair)
		instance.array_4 = ArrayPointer.from_stream(stream, instance.context, instance.count_4, generated.formats.janitorsettings.compound.UIntPair.UIntPair)
		instance.array_5 = ArrayPointer.from_stream(stream, instance.context, instance.count_5, generated.formats.janitorsettings.compound.UIntPair.UIntPair)
		instance.array_6 = ArrayPointer.from_stream(stream, instance.context, instance.count_6, generated.formats.base.basic.Uint)
		instance.array_7 = ArrayPointer.from_stream(stream, instance.context, instance.count_7, generated.formats.base.basic.Uint)
		instance.array_8 = ArrayPointer.from_stream(stream, instance.context, instance.count_8, generated.formats.base.basic.Uint)
		instance.array_9 = ArrayPointer.from_stream(stream, instance.context, instance.count_9, generated.formats.base.basic.Float)
		instance.array_10 = ArrayPointer.from_stream(stream, instance.context, instance.count_10, generated.formats.base.basic.Float)
		instance.array_11 = ArrayPointer.from_stream(stream, instance.context, instance.count_11, generated.formats.base.basic.Float)
		instance.array_12 = ArrayPointer.from_stream(stream, instance.context, instance.count_12, generated.formats.base.basic.Float)
		instance.array_13 = ArrayPointer.from_stream(stream, instance.context, instance.count_13, generated.formats.base.basic.Float)
		instance.array_14 = ArrayPointer.from_stream(stream, instance.context, instance.count_14, generated.formats.base.basic.Float)
		instance.unk_0 = stream.read_float()
		instance.unk_1 = stream.read_float()
		instance.unk_2 = stream.read_float()
		instance.unk_3 = stream.read_float()
		instance.unk_4 = stream.read_float()
		instance.unk_5 = stream.read_float()
		instance.unk_6 = stream.read_float()
		instance.unk_7 = stream.read_float()
		instance.unk_8 = stream.read_uint()
		instance.unk_9 = stream.read_float()
		instance.unk_10 = stream.read_float()
		instance.count_0 = stream.read_ubyte()
		instance.count_1 = stream.read_ubyte()
		instance.count_2 = stream.read_ubyte()
		instance.count_3 = stream.read_ubyte()
		instance.count_4 = stream.read_ubyte()
		instance.count_5 = stream.read_ubyte()
		instance.count_6 = stream.read_ubyte()
		instance.count_7 = stream.read_ubyte()
		instance.count_8 = stream.read_ubyte()
		instance.count_9 = stream.read_ubyte()
		instance.count_10 = stream.read_ubyte()
		instance.count_11 = stream.read_ubyte()
		instance.count_12 = stream.read_ubyte()
		instance.count_13 = stream.read_ubyte()
		instance.count_14 = stream.read_ubyte()
		instance.possibly_unused_count_0 = stream.read_ubyte()
		instance.possibly_unused_count_1 = stream.read_ubyte()
		instance.possibly_unused_count_2 = stream.read_ubyte()
		instance.possibly_unused_count_3 = stream.read_ubyte()
		instance.possibly_unused_count_4 = stream.read_ubyte()
		instance.unk_11 = stream.read_float()
		instance.unk_12 = stream.read_float()
		instance.unk_13 = stream.read_float()
		instance.unk_14 = stream.read_float()
		instance.unk_15 = stream.read_float()
		instance.unk_16 = stream.read_float()
		instance.unk_17 = stream.read_float()
		instance.unk_18 = stream.read_float()
		instance.unk_19 = stream.read_float()
		instance.unk_20 = stream.read_float()
		instance.unk_21 = stream.read_float()
		instance.unk_22 = stream.read_float()
		instance.unk_23 = stream.read_float()
		instance.unk_24 = stream.read_float()
		instance.unk_25 = stream.read_float()
		instance.unk_26 = stream.read_float()
		instance.unk_27 = stream.read_float()
		instance.unk_28 = stream.read_float()
		instance.unk_29 = stream.read_float()
		instance.unk_30 = stream.read_float()
		instance.unk_31 = stream.read_float()
		instance.unk_32 = stream.read_float()
		instance.array_0.arg = instance.count_0
		instance.array_1.arg = instance.count_1
		instance.array_2.arg = instance.count_2
		instance.array_3.arg = instance.count_3
		instance.array_4.arg = instance.count_4
		instance.array_5.arg = instance.count_5
		instance.array_6.arg = instance.count_6
		instance.array_7.arg = instance.count_7
		instance.array_8.arg = instance.count_8
		instance.array_9.arg = instance.count_9
		instance.array_10.arg = instance.count_10
		instance.array_11.arg = instance.count_11
		instance.array_12.arg = instance.count_12
		instance.array_13.arg = instance.count_13
		instance.array_14.arg = instance.count_14

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		ArrayPointer.to_stream(stream, instance.array_0)
		ArrayPointer.to_stream(stream, instance.array_1)
		ArrayPointer.to_stream(stream, instance.array_2)
		ArrayPointer.to_stream(stream, instance.array_3)
		ArrayPointer.to_stream(stream, instance.array_4)
		ArrayPointer.to_stream(stream, instance.array_5)
		ArrayPointer.to_stream(stream, instance.array_6)
		ArrayPointer.to_stream(stream, instance.array_7)
		ArrayPointer.to_stream(stream, instance.array_8)
		ArrayPointer.to_stream(stream, instance.array_9)
		ArrayPointer.to_stream(stream, instance.array_10)
		ArrayPointer.to_stream(stream, instance.array_11)
		ArrayPointer.to_stream(stream, instance.array_12)
		ArrayPointer.to_stream(stream, instance.array_13)
		ArrayPointer.to_stream(stream, instance.array_14)
		stream.write_float(instance.unk_0)
		stream.write_float(instance.unk_1)
		stream.write_float(instance.unk_2)
		stream.write_float(instance.unk_3)
		stream.write_float(instance.unk_4)
		stream.write_float(instance.unk_5)
		stream.write_float(instance.unk_6)
		stream.write_float(instance.unk_7)
		stream.write_uint(instance.unk_8)
		stream.write_float(instance.unk_9)
		stream.write_float(instance.unk_10)
		stream.write_ubyte(instance.count_0)
		stream.write_ubyte(instance.count_1)
		stream.write_ubyte(instance.count_2)
		stream.write_ubyte(instance.count_3)
		stream.write_ubyte(instance.count_4)
		stream.write_ubyte(instance.count_5)
		stream.write_ubyte(instance.count_6)
		stream.write_ubyte(instance.count_7)
		stream.write_ubyte(instance.count_8)
		stream.write_ubyte(instance.count_9)
		stream.write_ubyte(instance.count_10)
		stream.write_ubyte(instance.count_11)
		stream.write_ubyte(instance.count_12)
		stream.write_ubyte(instance.count_13)
		stream.write_ubyte(instance.count_14)
		stream.write_ubyte(instance.possibly_unused_count_0)
		stream.write_ubyte(instance.possibly_unused_count_1)
		stream.write_ubyte(instance.possibly_unused_count_2)
		stream.write_ubyte(instance.possibly_unused_count_3)
		stream.write_ubyte(instance.possibly_unused_count_4)
		stream.write_float(instance.unk_11)
		stream.write_float(instance.unk_12)
		stream.write_float(instance.unk_13)
		stream.write_float(instance.unk_14)
		stream.write_float(instance.unk_15)
		stream.write_float(instance.unk_16)
		stream.write_float(instance.unk_17)
		stream.write_float(instance.unk_18)
		stream.write_float(instance.unk_19)
		stream.write_float(instance.unk_20)
		stream.write_float(instance.unk_21)
		stream.write_float(instance.unk_22)
		stream.write_float(instance.unk_23)
		stream.write_float(instance.unk_24)
		stream.write_float(instance.unk_25)
		stream.write_float(instance.unk_26)
		stream.write_float(instance.unk_27)
		stream.write_float(instance.unk_28)
		stream.write_float(instance.unk_29)
		stream.write_float(instance.unk_30)
		stream.write_float(instance.unk_31)
		stream.write_float(instance.unk_32)

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
		return f'JanitorSettingsRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* array_0 = {fmt_member(self.array_0, indent+1)}'
		s += f'\n	* array_1 = {fmt_member(self.array_1, indent+1)}'
		s += f'\n	* array_2 = {fmt_member(self.array_2, indent+1)}'
		s += f'\n	* array_3 = {fmt_member(self.array_3, indent+1)}'
		s += f'\n	* array_4 = {fmt_member(self.array_4, indent+1)}'
		s += f'\n	* array_5 = {fmt_member(self.array_5, indent+1)}'
		s += f'\n	* array_6 = {fmt_member(self.array_6, indent+1)}'
		s += f'\n	* array_7 = {fmt_member(self.array_7, indent+1)}'
		s += f'\n	* array_8 = {fmt_member(self.array_8, indent+1)}'
		s += f'\n	* array_9 = {fmt_member(self.array_9, indent+1)}'
		s += f'\n	* array_10 = {fmt_member(self.array_10, indent+1)}'
		s += f'\n	* array_11 = {fmt_member(self.array_11, indent+1)}'
		s += f'\n	* array_12 = {fmt_member(self.array_12, indent+1)}'
		s += f'\n	* array_13 = {fmt_member(self.array_13, indent+1)}'
		s += f'\n	* array_14 = {fmt_member(self.array_14, indent+1)}'
		s += f'\n	* unk_0 = {fmt_member(self.unk_0, indent+1)}'
		s += f'\n	* unk_1 = {fmt_member(self.unk_1, indent+1)}'
		s += f'\n	* unk_2 = {fmt_member(self.unk_2, indent+1)}'
		s += f'\n	* unk_3 = {fmt_member(self.unk_3, indent+1)}'
		s += f'\n	* unk_4 = {fmt_member(self.unk_4, indent+1)}'
		s += f'\n	* unk_5 = {fmt_member(self.unk_5, indent+1)}'
		s += f'\n	* unk_6 = {fmt_member(self.unk_6, indent+1)}'
		s += f'\n	* unk_7 = {fmt_member(self.unk_7, indent+1)}'
		s += f'\n	* unk_8 = {fmt_member(self.unk_8, indent+1)}'
		s += f'\n	* unk_9 = {fmt_member(self.unk_9, indent+1)}'
		s += f'\n	* unk_10 = {fmt_member(self.unk_10, indent+1)}'
		s += f'\n	* count_0 = {fmt_member(self.count_0, indent+1)}'
		s += f'\n	* count_1 = {fmt_member(self.count_1, indent+1)}'
		s += f'\n	* count_2 = {fmt_member(self.count_2, indent+1)}'
		s += f'\n	* count_3 = {fmt_member(self.count_3, indent+1)}'
		s += f'\n	* count_4 = {fmt_member(self.count_4, indent+1)}'
		s += f'\n	* count_5 = {fmt_member(self.count_5, indent+1)}'
		s += f'\n	* count_6 = {fmt_member(self.count_6, indent+1)}'
		s += f'\n	* count_7 = {fmt_member(self.count_7, indent+1)}'
		s += f'\n	* count_8 = {fmt_member(self.count_8, indent+1)}'
		s += f'\n	* count_9 = {fmt_member(self.count_9, indent+1)}'
		s += f'\n	* count_10 = {fmt_member(self.count_10, indent+1)}'
		s += f'\n	* count_11 = {fmt_member(self.count_11, indent+1)}'
		s += f'\n	* count_12 = {fmt_member(self.count_12, indent+1)}'
		s += f'\n	* count_13 = {fmt_member(self.count_13, indent+1)}'
		s += f'\n	* count_14 = {fmt_member(self.count_14, indent+1)}'
		s += f'\n	* possibly_unused_count_0 = {fmt_member(self.possibly_unused_count_0, indent+1)}'
		s += f'\n	* possibly_unused_count_1 = {fmt_member(self.possibly_unused_count_1, indent+1)}'
		s += f'\n	* possibly_unused_count_2 = {fmt_member(self.possibly_unused_count_2, indent+1)}'
		s += f'\n	* possibly_unused_count_3 = {fmt_member(self.possibly_unused_count_3, indent+1)}'
		s += f'\n	* possibly_unused_count_4 = {fmt_member(self.possibly_unused_count_4, indent+1)}'
		s += f'\n	* unk_11 = {fmt_member(self.unk_11, indent+1)}'
		s += f'\n	* unk_12 = {fmt_member(self.unk_12, indent+1)}'
		s += f'\n	* unk_13 = {fmt_member(self.unk_13, indent+1)}'
		s += f'\n	* unk_14 = {fmt_member(self.unk_14, indent+1)}'
		s += f'\n	* unk_15 = {fmt_member(self.unk_15, indent+1)}'
		s += f'\n	* unk_16 = {fmt_member(self.unk_16, indent+1)}'
		s += f'\n	* unk_17 = {fmt_member(self.unk_17, indent+1)}'
		s += f'\n	* unk_18 = {fmt_member(self.unk_18, indent+1)}'
		s += f'\n	* unk_19 = {fmt_member(self.unk_19, indent+1)}'
		s += f'\n	* unk_20 = {fmt_member(self.unk_20, indent+1)}'
		s += f'\n	* unk_21 = {fmt_member(self.unk_21, indent+1)}'
		s += f'\n	* unk_22 = {fmt_member(self.unk_22, indent+1)}'
		s += f'\n	* unk_23 = {fmt_member(self.unk_23, indent+1)}'
		s += f'\n	* unk_24 = {fmt_member(self.unk_24, indent+1)}'
		s += f'\n	* unk_25 = {fmt_member(self.unk_25, indent+1)}'
		s += f'\n	* unk_26 = {fmt_member(self.unk_26, indent+1)}'
		s += f'\n	* unk_27 = {fmt_member(self.unk_27, indent+1)}'
		s += f'\n	* unk_28 = {fmt_member(self.unk_28, indent+1)}'
		s += f'\n	* unk_29 = {fmt_member(self.unk_29, indent+1)}'
		s += f'\n	* unk_30 = {fmt_member(self.unk_30, indent+1)}'
		s += f'\n	* unk_31 = {fmt_member(self.unk_31, indent+1)}'
		s += f'\n	* unk_32 = {fmt_member(self.unk_32, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
