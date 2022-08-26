from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Perk(MemStruct):

	__name__ = 'Perk'

	_import_path = 'generated.formats.restaurantsettings.compounds.Perk'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
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
		self.label = Pointer(self.context, 0, ZString)
		self.desc = Pointer(self.context, 0, ZString)
		self.icon = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
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
		self.label = Pointer(self.context, 0, ZString)
		self.desc = Pointer(self.context, 0, ZString)
		self.icon = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.unk_0 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.building_cost = Uint64.from_stream(stream, instance.context, 0, None)
		instance.running_cost_base = Uint64.from_stream(stream, instance.context, 0, None)
		instance.running_cost_per_extension = Uint64.from_stream(stream, instance.context, 0, None)
		instance.unk_4 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_5 = Float.from_stream(stream, instance.context, 0, None)
		instance.label = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.desc = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.icon = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.unk_6 = Float.from_stream(stream, instance.context, 0, None)
		instance.appeal_adults = Float.from_stream(stream, instance.context, 0, None)
		instance.appeal_families = Float.from_stream(stream, instance.context, 0, None)
		instance.appeal_teenagers = Float.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.label, int):
			instance.label.arg = 0
		if not isinstance(instance.desc, int):
			instance.desc.arg = 0
		if not isinstance(instance.icon, int):
			instance.icon.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.unk_0)
		Uint64.to_stream(stream, instance.building_cost)
		Uint64.to_stream(stream, instance.running_cost_base)
		Uint64.to_stream(stream, instance.running_cost_per_extension)
		Float.to_stream(stream, instance.unk_4)
		Float.to_stream(stream, instance.unk_5)
		Pointer.to_stream(stream, instance.label)
		Pointer.to_stream(stream, instance.desc)
		Pointer.to_stream(stream, instance.icon)
		Float.to_stream(stream, instance.unk_6)
		Float.to_stream(stream, instance.appeal_adults)
		Float.to_stream(stream, instance.appeal_families)
		Float.to_stream(stream, instance.appeal_teenagers)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'unk_0', Uint64, (0, None), (False, None)
		yield 'building_cost', Uint64, (0, None), (False, None)
		yield 'running_cost_base', Uint64, (0, None), (False, None)
		yield 'running_cost_per_extension', Uint64, (0, None), (False, None)
		yield 'unk_4', Float, (0, None), (False, None)
		yield 'unk_5', Float, (0, None), (False, None)
		yield 'label', Pointer, (0, ZString), (False, None)
		yield 'desc', Pointer, (0, ZString), (False, None)
		yield 'icon', Pointer, (0, ZString), (False, None)
		yield 'unk_6', Float, (0, None), (False, None)
		yield 'appeal_adults', Float, (0, None), (False, None)
		yield 'appeal_families', Float, (0, None), (False, None)
		yield 'appeal_teenagers', Float, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Perk [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* unk_0 = {self.fmt_member(self.unk_0, indent+1)}'
		s += f'\n	* building_cost = {self.fmt_member(self.building_cost, indent+1)}'
		s += f'\n	* running_cost_base = {self.fmt_member(self.running_cost_base, indent+1)}'
		s += f'\n	* running_cost_per_extension = {self.fmt_member(self.running_cost_per_extension, indent+1)}'
		s += f'\n	* unk_4 = {self.fmt_member(self.unk_4, indent+1)}'
		s += f'\n	* unk_5 = {self.fmt_member(self.unk_5, indent+1)}'
		s += f'\n	* label = {self.fmt_member(self.label, indent+1)}'
		s += f'\n	* desc = {self.fmt_member(self.desc, indent+1)}'
		s += f'\n	* icon = {self.fmt_member(self.icon, indent+1)}'
		s += f'\n	* unk_6 = {self.fmt_member(self.unk_6, indent+1)}'
		s += f'\n	* appeal_adults = {self.fmt_member(self.appeal_adults, indent+1)}'
		s += f'\n	* appeal_families = {self.fmt_member(self.appeal_families, indent+1)}'
		s += f'\n	* appeal_teenagers = {self.fmt_member(self.appeal_teenagers, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
