from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class JanitorSettingsRoot(MemStruct):

	"""
	huge batch of arrays at the head of the file
	"""

	__name__ = 'JanitorSettingsRoot'

	_import_key = 'janitorsettings.compounds.JanitorSettingsRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
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
		self.array_0 = ArrayPointer(self.context, self.count_0, JanitorSettingsRoot._import_map["janitorsettings.compounds.UIntPair"])
		self.array_1 = ArrayPointer(self.context, self.count_1, JanitorSettingsRoot._import_map["janitorsettings.compounds.UIntPair"])
		self.array_2 = ArrayPointer(self.context, self.count_2, JanitorSettingsRoot._import_map["janitorsettings.compounds.UIntPair"])
		self.array_3 = ArrayPointer(self.context, self.count_3, JanitorSettingsRoot._import_map["janitorsettings.compounds.UIntPair"])
		self.array_4 = ArrayPointer(self.context, self.count_4, JanitorSettingsRoot._import_map["janitorsettings.compounds.UIntPair"])
		self.array_5 = ArrayPointer(self.context, self.count_5, JanitorSettingsRoot._import_map["janitorsettings.compounds.UIntPair"])
		self.array_6 = ArrayPointer(self.context, self.count_6, Uint)
		self.array_7 = ArrayPointer(self.context, self.count_7, Uint)
		self.array_8 = ArrayPointer(self.context, self.count_8, Uint)
		self.array_9 = ArrayPointer(self.context, self.count_9, Float)
		self.array_10 = ArrayPointer(self.context, self.count_10, Float)
		self.array_11 = ArrayPointer(self.context, self.count_11, Float)
		self.array_12 = ArrayPointer(self.context, self.count_12, Float)
		self.array_13 = ArrayPointer(self.context, self.count_13, Float)
		self.array_14 = ArrayPointer(self.context, self.count_14, Float)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'array_0', ArrayPointer, (instance.count_0, JanitorSettingsRoot._import_map["janitorsettings.compounds.UIntPair"]), (False, None)
		yield 'array_1', ArrayPointer, (instance.count_1, JanitorSettingsRoot._import_map["janitorsettings.compounds.UIntPair"]), (False, None)
		yield 'array_2', ArrayPointer, (instance.count_2, JanitorSettingsRoot._import_map["janitorsettings.compounds.UIntPair"]), (False, None)
		yield 'array_3', ArrayPointer, (instance.count_3, JanitorSettingsRoot._import_map["janitorsettings.compounds.UIntPair"]), (False, None)
		yield 'array_4', ArrayPointer, (instance.count_4, JanitorSettingsRoot._import_map["janitorsettings.compounds.UIntPair"]), (False, None)
		yield 'array_5', ArrayPointer, (instance.count_5, JanitorSettingsRoot._import_map["janitorsettings.compounds.UIntPair"]), (False, None)
		yield 'array_6', ArrayPointer, (instance.count_6, Uint), (False, None)
		yield 'array_7', ArrayPointer, (instance.count_7, Uint), (False, None)
		yield 'array_8', ArrayPointer, (instance.count_8, Uint), (False, None)
		yield 'array_9', ArrayPointer, (instance.count_9, Float), (False, None)
		yield 'array_10', ArrayPointer, (instance.count_10, Float), (False, None)
		yield 'array_11', ArrayPointer, (instance.count_11, Float), (False, None)
		yield 'array_12', ArrayPointer, (instance.count_12, Float), (False, None)
		yield 'array_13', ArrayPointer, (instance.count_13, Float), (False, None)
		yield 'array_14', ArrayPointer, (instance.count_14, Float), (False, None)
		yield 'unk_0', Float, (0, None), (False, None)
		yield 'unk_1', Float, (0, None), (False, None)
		yield 'unk_2', Float, (0, None), (False, None)
		yield 'unk_3', Float, (0, None), (False, None)
		yield 'unk_4', Float, (0, None), (False, None)
		yield 'unk_5', Float, (0, None), (False, None)
		yield 'unk_6', Float, (0, None), (False, None)
		yield 'unk_7', Float, (0, None), (False, None)
		yield 'unk_8', Uint, (0, None), (False, None)
		yield 'unk_9', Float, (0, None), (False, None)
		yield 'unk_10', Float, (0, None), (False, None)
		yield 'count_0', Ubyte, (0, None), (False, None)
		yield 'count_1', Ubyte, (0, None), (False, None)
		yield 'count_2', Ubyte, (0, None), (False, None)
		yield 'count_3', Ubyte, (0, None), (False, None)
		yield 'count_4', Ubyte, (0, None), (False, None)
		yield 'count_5', Ubyte, (0, None), (False, None)
		yield 'count_6', Ubyte, (0, None), (False, None)
		yield 'count_7', Ubyte, (0, None), (False, None)
		yield 'count_8', Ubyte, (0, None), (False, None)
		yield 'count_9', Ubyte, (0, None), (False, None)
		yield 'count_10', Ubyte, (0, None), (False, None)
		yield 'count_11', Ubyte, (0, None), (False, None)
		yield 'count_12', Ubyte, (0, None), (False, None)
		yield 'count_13', Ubyte, (0, None), (False, None)
		yield 'count_14', Ubyte, (0, None), (False, None)
		yield 'possibly_unused_count_0', Ubyte, (0, None), (False, None)
		yield 'possibly_unused_count_1', Ubyte, (0, None), (False, None)
		yield 'possibly_unused_count_2', Ubyte, (0, None), (False, None)
		yield 'possibly_unused_count_3', Ubyte, (0, None), (False, None)
		yield 'possibly_unused_count_4', Ubyte, (0, None), (False, None)
		yield 'unk_11', Float, (0, None), (False, None)
		yield 'unk_12', Float, (0, None), (False, None)
		yield 'unk_13', Float, (0, None), (False, None)
		yield 'unk_14', Float, (0, None), (False, None)
		yield 'unk_15', Float, (0, None), (False, None)
		yield 'unk_16', Float, (0, None), (False, None)
		yield 'unk_17', Float, (0, None), (False, None)
		yield 'unk_18', Float, (0, None), (False, None)
		yield 'unk_19', Float, (0, None), (False, None)
		yield 'unk_20', Float, (0, None), (False, None)
		yield 'unk_21', Float, (0, None), (False, None)
		yield 'unk_22', Float, (0, None), (False, None)
		yield 'unk_23', Float, (0, None), (False, None)
		yield 'unk_24', Float, (0, None), (False, None)
		yield 'unk_25', Float, (0, None), (False, None)
		yield 'unk_26', Float, (0, None), (False, None)
		yield 'unk_27', Float, (0, None), (False, None)
		yield 'unk_28', Float, (0, None), (False, None)
		yield 'unk_29', Float, (0, None), (False, None)
		yield 'unk_30', Float, (0, None), (False, None)
		yield 'unk_31', Float, (0, None), (False, None)
		yield 'unk_32', Float, (0, None), (False, None)
