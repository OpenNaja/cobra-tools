from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class RestaurantSettingsRoot(MemStruct):

	__name__ = 'RestaurantSettingsRoot'

	_import_key = 'restaurantsettings.compounds.RestaurantSettingsRoot'

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
		self.perks = ArrayPointer(self.context, self.count, RestaurantSettingsRoot._import_map["restaurantsettings.compounds.Perk"])
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('running_cost_base', Uint64, (0, None), (False, None), None),
		('unk_1', Uint, (0, None), (False, None), None),
		('unk_2', Float, (0, None), (False, None), None),
		('unk_3', Float, (0, None), (False, None), None),
		('unk_4', Float, (0, None), (False, None), None),
		('unk_5', Float, (0, None), (False, None), None),
		('unk_6', Float, (0, None), (False, None), None),
		('running_cost_per_extension', Uint64, (0, None), (False, None), None),
		('unk_8', Uint, (0, None), (False, None), None),
		('unk_9', Float, (0, None), (False, None), None),
		('perks', ArrayPointer, (None, None), (False, None), None),
		('count', Uint64, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
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
		yield 'perks', ArrayPointer, (instance.count, RestaurantSettingsRoot._import_map["restaurantsettings.compounds.Perk"]), (False, None)
		yield 'count', Uint64, (0, None), (False, None)
