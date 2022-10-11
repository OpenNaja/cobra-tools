from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ContextSet1Item(MemStruct):

	__name__ = 'ContextSet1Item'

	_import_key = 'frendercontextset.compounds.ContextSet1Item'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.stuff_11_sub_count = 0
		self.stuff_12_sub_count = 0
		self.stuff_13_sub_count = 0
		self.stuff_1_unknown_1 = 0
		self.stuff_1_unknown_2 = 0
		self.stuff_1_name = Pointer(self.context, 0, ZString)
		self.stuff_11_sub = ArrayPointer(self.context, self.stuff_11_sub_count, ContextSet1Item._import_map["frendercontextset.compounds.ContextSet1SubItem"])
		self.stuff_12_sub = ArrayPointer(self.context, self.stuff_12_sub_count, ContextSet1Item._import_map["frendercontextset.compounds.ContextSet1SubItem"])
		self.stuff_13_sub = ArrayPointer(self.context, self.stuff_13_sub_count, ContextSet1Item._import_map["frendercontextset.compounds.ContextSet1SubItem"])
		self.stuff_14_sub_name = Pointer(self.context, 0, ZString)
		self.stuff_15_sub_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('stuff_1_name', Pointer, (0, ZString), (False, None), None),
		('stuff_11_sub', ArrayPointer, (None, None), (False, None), None),
		('stuff_11_sub_count', Uint64, (0, None), (False, None), None),
		('stuff_12_sub', ArrayPointer, (None, None), (False, None), None),
		('stuff_12_sub_count', Uint64, (0, None), (False, None), None),
		('stuff_13_sub', ArrayPointer, (None, None), (False, None), None),
		('stuff_13_sub_count', Uint64, (0, None), (False, None), None),
		('stuff_14_sub_name', Pointer, (0, ZString), (False, None), None),
		('stuff_14_sub_name', Pointer, (0, ZString), (False, None), None),
		('stuff_15_sub_name', Pointer, (0, ZString), (False, None), None),
		('stuff_1_unknown_1', Uint64, (0, None), (False, None), None),
		('stuff_1_unknown_2', Uint64, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'stuff_1_name', Pointer, (0, ZString), (False, None)
		yield 'stuff_11_sub', ArrayPointer, (instance.stuff_11_sub_count, ContextSet1Item._import_map["frendercontextset.compounds.ContextSet1SubItem"]), (False, None)
		yield 'stuff_11_sub_count', Uint64, (0, None), (False, None)
		yield 'stuff_12_sub', ArrayPointer, (instance.stuff_12_sub_count, ContextSet1Item._import_map["frendercontextset.compounds.ContextSet1SubItem"]), (False, None)
		yield 'stuff_12_sub_count', Uint64, (0, None), (False, None)
		yield 'stuff_13_sub', ArrayPointer, (instance.stuff_13_sub_count, ContextSet1Item._import_map["frendercontextset.compounds.ContextSet1SubItem"]), (False, None)
		yield 'stuff_13_sub_count', Uint64, (0, None), (False, None)
		yield 'stuff_14_sub_name', Pointer, (0, ZString), (False, None)
		yield 'stuff_14_sub_name', Pointer, (0, ZString), (False, None)
		yield 'stuff_15_sub_name', Pointer, (0, ZString), (False, None)
		yield 'stuff_1_unknown_1', Uint64, (0, None), (False, None)
		yield 'stuff_1_unknown_2', Uint64, (0, None), (False, None)
