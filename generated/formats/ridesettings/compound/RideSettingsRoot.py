from source.formats.base.basic import fmt_member
import generated.formats.ridesettings.compound.Pair
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class RideSettingsRoot(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.unk_0 = 0.0
		self.unk_1 = 0
		self.count = 0
		self.pad_0 = 0
		self.pad_1 = 0
		self.pad_2 = 0
		self.array_1 = ArrayPointer(self.context, self.count, generated.formats.ridesettings.compound.Pair.Pair)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.unk_0 = 0.0
		self.unk_1 = 0
		self.count = 0
		self.pad_0 = 0
		self.pad_1 = 0
		self.pad_2 = 0
		self.array_1 = ArrayPointer(self.context, self.count, generated.formats.ridesettings.compound.Pair.Pair)

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
		instance.unk_0 = stream.read_float()
		instance.unk_1 = stream.read_uint()
		instance.array_1 = ArrayPointer.from_stream(stream, instance.context, instance.count, generated.formats.ridesettings.compound.Pair.Pair)
		instance.count = stream.read_uint()
		instance.pad_0 = stream.read_uint()
		instance.pad_1 = stream.read_uint()
		instance.pad_2 = stream.read_uint()
		instance.array_1.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_float(instance.unk_0)
		stream.write_uint(instance.unk_1)
		ArrayPointer.to_stream(stream, instance.array_1)
		stream.write_uint(instance.count)
		stream.write_uint(instance.pad_0)
		stream.write_uint(instance.pad_1)
		stream.write_uint(instance.pad_2)

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
		return f'RideSettingsRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* unk_0 = {fmt_member(self.unk_0, indent+1)}'
		s += f'\n	* unk_1 = {fmt_member(self.unk_1, indent+1)}'
		s += f'\n	* array_1 = {fmt_member(self.array_1, indent+1)}'
		s += f'\n	* count = {fmt_member(self.count, indent+1)}'
		s += f'\n	* pad_0 = {fmt_member(self.pad_0, indent+1)}'
		s += f'\n	* pad_1 = {fmt_member(self.pad_1, indent+1)}'
		s += f'\n	* pad_2 = {fmt_member(self.pad_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
