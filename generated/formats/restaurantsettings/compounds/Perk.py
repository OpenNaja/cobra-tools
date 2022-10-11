from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Perk(MemStruct):

	__name__ = 'Perk'

	_import_key = 'restaurantsettings.compounds.Perk'

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

	_attribute_list = MemStruct._attribute_list + [
		('unk_0', Uint64, (0, None), (False, None), None),
		('building_cost', Uint64, (0, None), (False, None), None),
		('running_cost_base', Uint64, (0, None), (False, None), None),
		('running_cost_per_extension', Uint64, (0, None), (False, None), None),
		('unk_4', Float, (0, None), (False, None), None),
		('unk_5', Float, (0, None), (False, None), None),
		('label', Pointer, (0, ZString), (False, None), None),
		('desc', Pointer, (0, ZString), (False, None), None),
		('icon', Pointer, (0, ZString), (False, None), None),
		('unk_6', Float, (0, None), (False, None), None),
		('appeal_adults', Float, (0, None), (False, None), None),
		('appeal_families', Float, (0, None), (False, None), None),
		('appeal_teenagers', Float, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
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
