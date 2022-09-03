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

	_import_path = 'generated.formats.janitorsettings.compounds.JanitorSettingsRoot'

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
		self.array_0 = ArrayPointer(self.context, self.count_0, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		self.array_1 = ArrayPointer(self.context, self.count_1, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		self.array_2 = ArrayPointer(self.context, self.count_2, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		self.array_3 = ArrayPointer(self.context, self.count_3, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		self.array_4 = ArrayPointer(self.context, self.count_4, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		self.array_5 = ArrayPointer(self.context, self.count_5, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
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

	def set_defaults(self):
		super().set_defaults()
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
		self.array_0 = ArrayPointer(self.context, self.count_0, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		self.array_1 = ArrayPointer(self.context, self.count_1, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		self.array_2 = ArrayPointer(self.context, self.count_2, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		self.array_3 = ArrayPointer(self.context, self.count_3, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		self.array_4 = ArrayPointer(self.context, self.count_4, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		self.array_5 = ArrayPointer(self.context, self.count_5, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		self.array_6 = ArrayPointer(self.context, self.count_6, Uint)
		self.array_7 = ArrayPointer(self.context, self.count_7, Uint)
		self.array_8 = ArrayPointer(self.context, self.count_8, Uint)
		self.array_9 = ArrayPointer(self.context, self.count_9, Float)
		self.array_10 = ArrayPointer(self.context, self.count_10, Float)
		self.array_11 = ArrayPointer(self.context, self.count_11, Float)
		self.array_12 = ArrayPointer(self.context, self.count_12, Float)
		self.array_13 = ArrayPointer(self.context, self.count_13, Float)
		self.array_14 = ArrayPointer(self.context, self.count_14, Float)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.array_0 = ArrayPointer.from_stream(stream, instance.context, instance.count_0, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		instance.array_1 = ArrayPointer.from_stream(stream, instance.context, instance.count_1, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		instance.array_2 = ArrayPointer.from_stream(stream, instance.context, instance.count_2, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		instance.array_3 = ArrayPointer.from_stream(stream, instance.context, instance.count_3, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		instance.array_4 = ArrayPointer.from_stream(stream, instance.context, instance.count_4, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		instance.array_5 = ArrayPointer.from_stream(stream, instance.context, instance.count_5, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"])
		instance.array_6 = ArrayPointer.from_stream(stream, instance.context, instance.count_6, Uint)
		instance.array_7 = ArrayPointer.from_stream(stream, instance.context, instance.count_7, Uint)
		instance.array_8 = ArrayPointer.from_stream(stream, instance.context, instance.count_8, Uint)
		instance.array_9 = ArrayPointer.from_stream(stream, instance.context, instance.count_9, Float)
		instance.array_10 = ArrayPointer.from_stream(stream, instance.context, instance.count_10, Float)
		instance.array_11 = ArrayPointer.from_stream(stream, instance.context, instance.count_11, Float)
		instance.array_12 = ArrayPointer.from_stream(stream, instance.context, instance.count_12, Float)
		instance.array_13 = ArrayPointer.from_stream(stream, instance.context, instance.count_13, Float)
		instance.array_14 = ArrayPointer.from_stream(stream, instance.context, instance.count_14, Float)
		instance.unk_0 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_1 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_2 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_3 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_4 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_5 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_6 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_7 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_8 = Uint.from_stream(stream, instance.context, 0, None)
		instance.unk_9 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_10 = Float.from_stream(stream, instance.context, 0, None)
		instance.count_0 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_1 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_2 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_3 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_4 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_5 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_6 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_7 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_8 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_9 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_10 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_11 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_12 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_13 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_14 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.possibly_unused_count_0 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.possibly_unused_count_1 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.possibly_unused_count_2 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.possibly_unused_count_3 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.possibly_unused_count_4 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.unk_11 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_12 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_13 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_14 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_15 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_16 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_17 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_18 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_19 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_20 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_21 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_22 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_23 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_24 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_25 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_26 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_27 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_28 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_29 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_30 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_31 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_32 = Float.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.array_0, int):
			instance.array_0.arg = instance.count_0
		if not isinstance(instance.array_1, int):
			instance.array_1.arg = instance.count_1
		if not isinstance(instance.array_2, int):
			instance.array_2.arg = instance.count_2
		if not isinstance(instance.array_3, int):
			instance.array_3.arg = instance.count_3
		if not isinstance(instance.array_4, int):
			instance.array_4.arg = instance.count_4
		if not isinstance(instance.array_5, int):
			instance.array_5.arg = instance.count_5
		if not isinstance(instance.array_6, int):
			instance.array_6.arg = instance.count_6
		if not isinstance(instance.array_7, int):
			instance.array_7.arg = instance.count_7
		if not isinstance(instance.array_8, int):
			instance.array_8.arg = instance.count_8
		if not isinstance(instance.array_9, int):
			instance.array_9.arg = instance.count_9
		if not isinstance(instance.array_10, int):
			instance.array_10.arg = instance.count_10
		if not isinstance(instance.array_11, int):
			instance.array_11.arg = instance.count_11
		if not isinstance(instance.array_12, int):
			instance.array_12.arg = instance.count_12
		if not isinstance(instance.array_13, int):
			instance.array_13.arg = instance.count_13
		if not isinstance(instance.array_14, int):
			instance.array_14.arg = instance.count_14

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		ArrayPointer.to_stream(stream, instance.array_0)
		ArrayPointer.to_stream(stream, instance.array_1)
		ArrayPointer.to_stream(stream, instance.array_2)
		ArrayPointer.to_stream(stream, instance.array_3)
		ArrayPointer.to_stream(stream, instance.array_4)
		ArrayPointer.to_stream(stream, instance.array_5)
		ArrayPointer.to_stream(stream, instance.array_6)
		ArrayPointer.to_stream(stream, instance.array_7)
		ArrayPointer.to_stream(stream, instance.array_8)
		ArrayPointer.to_stream(stream, instance.array_9)
		ArrayPointer.to_stream(stream, instance.array_10)
		ArrayPointer.to_stream(stream, instance.array_11)
		ArrayPointer.to_stream(stream, instance.array_12)
		ArrayPointer.to_stream(stream, instance.array_13)
		ArrayPointer.to_stream(stream, instance.array_14)
		Float.to_stream(stream, instance.unk_0)
		Float.to_stream(stream, instance.unk_1)
		Float.to_stream(stream, instance.unk_2)
		Float.to_stream(stream, instance.unk_3)
		Float.to_stream(stream, instance.unk_4)
		Float.to_stream(stream, instance.unk_5)
		Float.to_stream(stream, instance.unk_6)
		Float.to_stream(stream, instance.unk_7)
		Uint.to_stream(stream, instance.unk_8)
		Float.to_stream(stream, instance.unk_9)
		Float.to_stream(stream, instance.unk_10)
		Ubyte.to_stream(stream, instance.count_0)
		Ubyte.to_stream(stream, instance.count_1)
		Ubyte.to_stream(stream, instance.count_2)
		Ubyte.to_stream(stream, instance.count_3)
		Ubyte.to_stream(stream, instance.count_4)
		Ubyte.to_stream(stream, instance.count_5)
		Ubyte.to_stream(stream, instance.count_6)
		Ubyte.to_stream(stream, instance.count_7)
		Ubyte.to_stream(stream, instance.count_8)
		Ubyte.to_stream(stream, instance.count_9)
		Ubyte.to_stream(stream, instance.count_10)
		Ubyte.to_stream(stream, instance.count_11)
		Ubyte.to_stream(stream, instance.count_12)
		Ubyte.to_stream(stream, instance.count_13)
		Ubyte.to_stream(stream, instance.count_14)
		Ubyte.to_stream(stream, instance.possibly_unused_count_0)
		Ubyte.to_stream(stream, instance.possibly_unused_count_1)
		Ubyte.to_stream(stream, instance.possibly_unused_count_2)
		Ubyte.to_stream(stream, instance.possibly_unused_count_3)
		Ubyte.to_stream(stream, instance.possibly_unused_count_4)
		Float.to_stream(stream, instance.unk_11)
		Float.to_stream(stream, instance.unk_12)
		Float.to_stream(stream, instance.unk_13)
		Float.to_stream(stream, instance.unk_14)
		Float.to_stream(stream, instance.unk_15)
		Float.to_stream(stream, instance.unk_16)
		Float.to_stream(stream, instance.unk_17)
		Float.to_stream(stream, instance.unk_18)
		Float.to_stream(stream, instance.unk_19)
		Float.to_stream(stream, instance.unk_20)
		Float.to_stream(stream, instance.unk_21)
		Float.to_stream(stream, instance.unk_22)
		Float.to_stream(stream, instance.unk_23)
		Float.to_stream(stream, instance.unk_24)
		Float.to_stream(stream, instance.unk_25)
		Float.to_stream(stream, instance.unk_26)
		Float.to_stream(stream, instance.unk_27)
		Float.to_stream(stream, instance.unk_28)
		Float.to_stream(stream, instance.unk_29)
		Float.to_stream(stream, instance.unk_30)
		Float.to_stream(stream, instance.unk_31)
		Float.to_stream(stream, instance.unk_32)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'array_0', ArrayPointer, (instance.count_0, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"]), (False, None)
		yield 'array_1', ArrayPointer, (instance.count_1, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"]), (False, None)
		yield 'array_2', ArrayPointer, (instance.count_2, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"]), (False, None)
		yield 'array_3', ArrayPointer, (instance.count_3, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"]), (False, None)
		yield 'array_4', ArrayPointer, (instance.count_4, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"]), (False, None)
		yield 'array_5', ArrayPointer, (instance.count_5, JanitorSettingsRoot._import_path_map["generated.formats.janitorsettings.compounds.UIntPair"]), (False, None)
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

	def get_info_str(self, indent=0):
		return f'JanitorSettingsRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* array_0 = {self.fmt_member(self.array_0, indent+1)}'
		s += f'\n	* array_1 = {self.fmt_member(self.array_1, indent+1)}'
		s += f'\n	* array_2 = {self.fmt_member(self.array_2, indent+1)}'
		s += f'\n	* array_3 = {self.fmt_member(self.array_3, indent+1)}'
		s += f'\n	* array_4 = {self.fmt_member(self.array_4, indent+1)}'
		s += f'\n	* array_5 = {self.fmt_member(self.array_5, indent+1)}'
		s += f'\n	* array_6 = {self.fmt_member(self.array_6, indent+1)}'
		s += f'\n	* array_7 = {self.fmt_member(self.array_7, indent+1)}'
		s += f'\n	* array_8 = {self.fmt_member(self.array_8, indent+1)}'
		s += f'\n	* array_9 = {self.fmt_member(self.array_9, indent+1)}'
		s += f'\n	* array_10 = {self.fmt_member(self.array_10, indent+1)}'
		s += f'\n	* array_11 = {self.fmt_member(self.array_11, indent+1)}'
		s += f'\n	* array_12 = {self.fmt_member(self.array_12, indent+1)}'
		s += f'\n	* array_13 = {self.fmt_member(self.array_13, indent+1)}'
		s += f'\n	* array_14 = {self.fmt_member(self.array_14, indent+1)}'
		s += f'\n	* unk_0 = {self.fmt_member(self.unk_0, indent+1)}'
		s += f'\n	* unk_1 = {self.fmt_member(self.unk_1, indent+1)}'
		s += f'\n	* unk_2 = {self.fmt_member(self.unk_2, indent+1)}'
		s += f'\n	* unk_3 = {self.fmt_member(self.unk_3, indent+1)}'
		s += f'\n	* unk_4 = {self.fmt_member(self.unk_4, indent+1)}'
		s += f'\n	* unk_5 = {self.fmt_member(self.unk_5, indent+1)}'
		s += f'\n	* unk_6 = {self.fmt_member(self.unk_6, indent+1)}'
		s += f'\n	* unk_7 = {self.fmt_member(self.unk_7, indent+1)}'
		s += f'\n	* unk_8 = {self.fmt_member(self.unk_8, indent+1)}'
		s += f'\n	* unk_9 = {self.fmt_member(self.unk_9, indent+1)}'
		s += f'\n	* unk_10 = {self.fmt_member(self.unk_10, indent+1)}'
		s += f'\n	* count_0 = {self.fmt_member(self.count_0, indent+1)}'
		s += f'\n	* count_1 = {self.fmt_member(self.count_1, indent+1)}'
		s += f'\n	* count_2 = {self.fmt_member(self.count_2, indent+1)}'
		s += f'\n	* count_3 = {self.fmt_member(self.count_3, indent+1)}'
		s += f'\n	* count_4 = {self.fmt_member(self.count_4, indent+1)}'
		s += f'\n	* count_5 = {self.fmt_member(self.count_5, indent+1)}'
		s += f'\n	* count_6 = {self.fmt_member(self.count_6, indent+1)}'
		s += f'\n	* count_7 = {self.fmt_member(self.count_7, indent+1)}'
		s += f'\n	* count_8 = {self.fmt_member(self.count_8, indent+1)}'
		s += f'\n	* count_9 = {self.fmt_member(self.count_9, indent+1)}'
		s += f'\n	* count_10 = {self.fmt_member(self.count_10, indent+1)}'
		s += f'\n	* count_11 = {self.fmt_member(self.count_11, indent+1)}'
		s += f'\n	* count_12 = {self.fmt_member(self.count_12, indent+1)}'
		s += f'\n	* count_13 = {self.fmt_member(self.count_13, indent+1)}'
		s += f'\n	* count_14 = {self.fmt_member(self.count_14, indent+1)}'
		s += f'\n	* possibly_unused_count_0 = {self.fmt_member(self.possibly_unused_count_0, indent+1)}'
		s += f'\n	* possibly_unused_count_1 = {self.fmt_member(self.possibly_unused_count_1, indent+1)}'
		s += f'\n	* possibly_unused_count_2 = {self.fmt_member(self.possibly_unused_count_2, indent+1)}'
		s += f'\n	* possibly_unused_count_3 = {self.fmt_member(self.possibly_unused_count_3, indent+1)}'
		s += f'\n	* possibly_unused_count_4 = {self.fmt_member(self.possibly_unused_count_4, indent+1)}'
		s += f'\n	* unk_11 = {self.fmt_member(self.unk_11, indent+1)}'
		s += f'\n	* unk_12 = {self.fmt_member(self.unk_12, indent+1)}'
		s += f'\n	* unk_13 = {self.fmt_member(self.unk_13, indent+1)}'
		s += f'\n	* unk_14 = {self.fmt_member(self.unk_14, indent+1)}'
		s += f'\n	* unk_15 = {self.fmt_member(self.unk_15, indent+1)}'
		s += f'\n	* unk_16 = {self.fmt_member(self.unk_16, indent+1)}'
		s += f'\n	* unk_17 = {self.fmt_member(self.unk_17, indent+1)}'
		s += f'\n	* unk_18 = {self.fmt_member(self.unk_18, indent+1)}'
		s += f'\n	* unk_19 = {self.fmt_member(self.unk_19, indent+1)}'
		s += f'\n	* unk_20 = {self.fmt_member(self.unk_20, indent+1)}'
		s += f'\n	* unk_21 = {self.fmt_member(self.unk_21, indent+1)}'
		s += f'\n	* unk_22 = {self.fmt_member(self.unk_22, indent+1)}'
		s += f'\n	* unk_23 = {self.fmt_member(self.unk_23, indent+1)}'
		s += f'\n	* unk_24 = {self.fmt_member(self.unk_24, indent+1)}'
		s += f'\n	* unk_25 = {self.fmt_member(self.unk_25, indent+1)}'
		s += f'\n	* unk_26 = {self.fmt_member(self.unk_26, indent+1)}'
		s += f'\n	* unk_27 = {self.fmt_member(self.unk_27, indent+1)}'
		s += f'\n	* unk_28 = {self.fmt_member(self.unk_28, indent+1)}'
		s += f'\n	* unk_29 = {self.fmt_member(self.unk_29, indent+1)}'
		s += f'\n	* unk_30 = {self.fmt_member(self.unk_30, indent+1)}'
		s += f'\n	* unk_31 = {self.fmt_member(self.unk_31, indent+1)}'
		s += f'\n	* unk_32 = {self.fmt_member(self.unk_32, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
