from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class LodSpecItem(MemStruct):

	__name__ = 'LodSpecItem'

	_import_key = 'frenderlodspec.compounds.LodSpecItem'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unknown_1 = 0
		self.distance = 0.0
		self.flags_1 = 0
		self.flags_2 = 0
		self.float_1 = 0.0
		self.float_2 = 0.0
		self.float_3 = 0.0
		self.float_4 = 0.0
		self.float_5 = 0.0
		self.float_6 = 0.0
		self.unknown_2 = 0
		self.unknown_3 = 0
		self.unknown_4 = 0
		self.spec_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('spec_name', Pointer, (0, ZString), (False, None), None),
		('unknown_1', Uint, (0, None), (False, None), None),
		('distance', Float, (0, None), (False, None), None),
		('flags_1', Ushort, (0, None), (False, None), None),
		('flags_2', Ushort, (0, None), (False, None), None),
		('float_1', Float, (0, None), (False, None), None),
		('float_2', Float, (0, None), (False, None), None),
		('float_3', Float, (0, None), (False, None), None),
		('float_4', Float, (0, None), (False, None), None),
		('float_5', Float, (0, None), (False, None), None),
		('float_6', Float, (0, None), (False, None), None),
		('unknown_2', Uint, (0, None), (False, None), None),
		('unknown_3', Uint, (0, None), (False, None), None),
		('unknown_4', Uint, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'spec_name', Pointer, (0, ZString), (False, None)
		yield 'unknown_1', Uint, (0, None), (False, None)
		yield 'distance', Float, (0, None), (False, None)
		yield 'flags_1', Ushort, (0, None), (False, None)
		yield 'flags_2', Ushort, (0, None), (False, None)
		yield 'float_1', Float, (0, None), (False, None)
		yield 'float_2', Float, (0, None), (False, None)
		yield 'float_3', Float, (0, None), (False, None)
		yield 'float_4', Float, (0, None), (False, None)
		yield 'float_5', Float, (0, None), (False, None)
		yield 'float_6', Float, (0, None), (False, None)
		yield 'unknown_2', Uint, (0, None), (False, None)
		yield 'unknown_3', Uint, (0, None), (False, None)
		yield 'unknown_4', Uint, (0, None), (False, None)
