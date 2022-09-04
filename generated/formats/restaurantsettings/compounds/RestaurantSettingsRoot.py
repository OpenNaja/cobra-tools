from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class RestaurantSettingsRoot(MemStruct):

	__name__ = 'RestaurantSettingsRoot'

	_import_path = 'generated.formats.restaurantsettings.compounds.RestaurantSettingsRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
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
		self.perks = ArrayPointer(self.context, self.count, RestaurantSettingsRoot._import_path_map["generated.formats.restaurantsettings.compounds.Perk"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
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
		self.perks = ArrayPointer(self.context, self.count, RestaurantSettingsRoot._import_path_map["generated.formats.restaurantsettings.compounds.Perk"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.running_cost_base = Uint64.from_stream(stream, instance.context, 0, None)
		instance.unk_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.unk_2 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_3 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_4 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_5 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_6 = Float.from_stream(stream, instance.context, 0, None)
		instance.running_cost_per_extension = Uint64.from_stream(stream, instance.context, 0, None)
		instance.unk_8 = Uint.from_stream(stream, instance.context, 0, None)
		instance.unk_9 = Float.from_stream(stream, instance.context, 0, None)
		instance.perks = ArrayPointer.from_stream(stream, instance.context, instance.count, RestaurantSettingsRoot._import_path_map["generated.formats.restaurantsettings.compounds.Perk"])
		instance.count = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.perks, int):
			instance.perks.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.running_cost_base)
		Uint.to_stream(stream, instance.unk_1)
		Float.to_stream(stream, instance.unk_2)
		Float.to_stream(stream, instance.unk_3)
		Float.to_stream(stream, instance.unk_4)
		Float.to_stream(stream, instance.unk_5)
		Float.to_stream(stream, instance.unk_6)
		Uint64.to_stream(stream, instance.running_cost_per_extension)
		Uint.to_stream(stream, instance.unk_8)
		Float.to_stream(stream, instance.unk_9)
		ArrayPointer.to_stream(stream, instance.perks)
		Uint64.to_stream(stream, instance.count)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'running_cost_base', Uint64, (0, None), (False, None)
		yield 'unk_1', Uint, (0, None), (False, None)
		yield 'unk_2', Float, (0, None), (False, None)
		yield 'unk_3', Float, (0, None), (False, None)
		yield 'unk_4', Float, (0, None), (False, None)
		yield 'unk_5', Float, (0, None), (False, None)
		yield 'unk_6', Float, (0, None), (False, None)
		yield 'running_cost_per_extension', Uint64, (0, None), (False, None)
		yield 'unk_8', Uint, (0, None), (False, None)
		yield 'unk_9', Float, (0, None), (False, None)
		yield 'perks', ArrayPointer, (instance.count, RestaurantSettingsRoot._import_path_map["generated.formats.restaurantsettings.compounds.Perk"]), (False, None)
		yield 'count', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'RestaurantSettingsRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
