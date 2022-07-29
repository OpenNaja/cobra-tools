from generated.formats.base.basic import fmt_member
import generated.formats.base.basic
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class Perk(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.unk_0 = 0
		self.building_cost = 0
		self.running_cost_base = 0
		self.running_cost_per_extension = 0
		self.unk_4 = 0
		self.unk_5 = 0
		self.unk_6 = 0
		self.appeal_adults = 0
		self.appeal_families = 0
		self.appeal_teenagers = 0
		self.label = 0
		self.desc = 0
		self.icon = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.unk_0 = 0
		self.building_cost = 0
		self.running_cost_base = 0
		self.running_cost_per_extension = 0
		self.unk_4 = 0.0
		self.unk_5 = 0.0
		self.unk_6 = 0.0
		self.appeal_adults = 0.0
		self.appeal_families = 0.0
		self.appeal_teenagers = 0.0
		self.label = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.desc = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.icon = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.unk_0 = stream.read_uint64()
		instance.building_cost = stream.read_uint64()
		instance.running_cost_base = stream.read_uint64()
		instance.running_cost_per_extension = stream.read_uint64()
		instance.unk_4 = stream.read_float()
		instance.unk_5 = stream.read_float()
		instance.label = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.desc = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.icon = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.unk_6 = stream.read_float()
		instance.appeal_adults = stream.read_float()
		instance.appeal_families = stream.read_float()
		instance.appeal_teenagers = stream.read_float()
		instance.label.arg = 0
		instance.desc.arg = 0
		instance.icon.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64(instance.unk_0)
		stream.write_uint64(instance.building_cost)
		stream.write_uint64(instance.running_cost_base)
		stream.write_uint64(instance.running_cost_per_extension)
		stream.write_float(instance.unk_4)
		stream.write_float(instance.unk_5)
		Pointer.to_stream(stream, instance.label)
		Pointer.to_stream(stream, instance.desc)
		Pointer.to_stream(stream, instance.icon)
		stream.write_float(instance.unk_6)
		stream.write_float(instance.appeal_adults)
		stream.write_float(instance.appeal_families)
		stream.write_float(instance.appeal_teenagers)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('unk_0', Uint64, (0, None))
		yield ('building_cost', Uint64, (0, None))
		yield ('running_cost_base', Uint64, (0, None))
		yield ('running_cost_per_extension', Uint64, (0, None))
		yield ('unk_4', Float, (0, None))
		yield ('unk_5', Float, (0, None))
		yield ('label', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('desc', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('icon', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('unk_6', Float, (0, None))
		yield ('appeal_adults', Float, (0, None))
		yield ('appeal_families', Float, (0, None))
		yield ('appeal_teenagers', Float, (0, None))

	def get_info_str(self, indent=0):
		return f'Perk [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* unk_0 = {fmt_member(self.unk_0, indent+1)}'
		s += f'\n	* building_cost = {fmt_member(self.building_cost, indent+1)}'
		s += f'\n	* running_cost_base = {fmt_member(self.running_cost_base, indent+1)}'
		s += f'\n	* running_cost_per_extension = {fmt_member(self.running_cost_per_extension, indent+1)}'
		s += f'\n	* unk_4 = {fmt_member(self.unk_4, indent+1)}'
		s += f'\n	* unk_5 = {fmt_member(self.unk_5, indent+1)}'
		s += f'\n	* label = {fmt_member(self.label, indent+1)}'
		s += f'\n	* desc = {fmt_member(self.desc, indent+1)}'
		s += f'\n	* icon = {fmt_member(self.icon, indent+1)}'
		s += f'\n	* unk_6 = {fmt_member(self.unk_6, indent+1)}'
		s += f'\n	* appeal_adults = {fmt_member(self.appeal_adults, indent+1)}'
		s += f'\n	* appeal_families = {fmt_member(self.appeal_families, indent+1)}'
		s += f'\n	* appeal_teenagers = {fmt_member(self.appeal_teenagers, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
