from source.formats.base.basic import fmt_member
import generated.formats.restaurantsettings.compound.Perk
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class RestaurantSettingsRoot(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.running_cost_base = 0
		self.unk_1 = 0
		self.unk_2 = 0
		self.unk_3 = 0
		self.unk_4 = 0
		self.unk_5 = 0
		self.unk_6 = 0
		self.running_cost_per_extension = 0
		self.unk_8 = 0
		self.unk_9 = 0
		self.count = 0
		self.perks = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.running_cost_base = 0
		self.unk_1 = 0
		self.unk_2 = 0.0
		self.unk_3 = 0.0
		self.unk_4 = 0.0
		self.unk_5 = 0.0
		self.unk_6 = 0.0
		self.running_cost_per_extension = 0
		self.unk_8 = 0
		self.unk_9 = 0.0
		self.count = 0
		self.perks = ArrayPointer(self.context, self.count, generated.formats.restaurantsettings.compound.Perk.Perk)

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
		instance.running_cost_base = stream.read_uint64()
		instance.unk_1 = stream.read_uint()
		instance.unk_2 = stream.read_float()
		instance.unk_3 = stream.read_float()
		instance.unk_4 = stream.read_float()
		instance.unk_5 = stream.read_float()
		instance.unk_6 = stream.read_float()
		instance.running_cost_per_extension = stream.read_uint64()
		instance.unk_8 = stream.read_uint()
		instance.unk_9 = stream.read_float()
		instance.perks = ArrayPointer.from_stream(stream, instance.context, instance.count, generated.formats.restaurantsettings.compound.Perk.Perk)
		instance.count = stream.read_uint64()
		instance.perks.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64(instance.running_cost_base)
		stream.write_uint(instance.unk_1)
		stream.write_float(instance.unk_2)
		stream.write_float(instance.unk_3)
		stream.write_float(instance.unk_4)
		stream.write_float(instance.unk_5)
		stream.write_float(instance.unk_6)
		stream.write_uint64(instance.running_cost_per_extension)
		stream.write_uint(instance.unk_8)
		stream.write_float(instance.unk_9)
		ArrayPointer.to_stream(stream, instance.perks)
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
		return f'RestaurantSettingsRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* running_cost_base = {fmt_member(self.running_cost_base, indent+1)}'
		s += f'\n	* unk_1 = {fmt_member(self.unk_1, indent+1)}'
		s += f'\n	* unk_2 = {fmt_member(self.unk_2, indent+1)}'
		s += f'\n	* unk_3 = {fmt_member(self.unk_3, indent+1)}'
		s += f'\n	* unk_4 = {fmt_member(self.unk_4, indent+1)}'
		s += f'\n	* unk_5 = {fmt_member(self.unk_5, indent+1)}'
		s += f'\n	* unk_6 = {fmt_member(self.unk_6, indent+1)}'
		s += f'\n	* running_cost_per_extension = {fmt_member(self.running_cost_per_extension, indent+1)}'
		s += f'\n	* unk_8 = {fmt_member(self.unk_8, indent+1)}'
		s += f'\n	* unk_9 = {fmt_member(self.unk_9, indent+1)}'
		s += f'\n	* perks = {fmt_member(self.perks, indent+1)}'
		s += f'\n	* count = {fmt_member(self.count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
