from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class CompressedManiData(BaseStruct):

	__name__ = 'CompressedManiData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ref = name_type_map['Empty'](self.context, 0, None)

		# these are likely a scale reference or factor
		self.floatsa = Array(self.context, 0, None, (0,), name_type_map['Float'])

		# ?
		self.pad_2 = name_type_map['SmartPadding'](self.context, 0, None)
		self.frame_count = name_type_map['Uint'](self.context, 0, None)
		self.ori_bone_count = name_type_map['Uint'](self.context, 0, None)
		self.pos_bone_count = name_type_map['Uint'](self.context, 0, None)

		# maybe
		self.scl_bone_count = name_type_map['Uint'](self.context, 0, None)

		# fixed
		self.zeros_18 = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.count = name_type_map['Ushort'](self.context, 0, None)

		# usually 420, or 0
		self.quantisation_level = name_type_map['Ushort'](self.context, 0, None)
		self.ref_2 = name_type_map['Empty'](self.context, 0, None)
		self.some_indices = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.flag_0 = name_type_map['Ubyte'](self.context, 0, None)
		self.flag_1 = name_type_map['Ubyte'](self.context, 0, None)
		self.flag_2 = name_type_map['Ubyte'](self.context, 0, None)
		self.flag_3 = name_type_map['Ubyte'](self.context, 0, None)
		self.anoth_pad = name_type_map['PadAlign'](self.context, 4, self.ref_2)

		# these are likely a scale reference or factor
		self.floatsb = name_type_map['FloatsGrabber'](self.context, 0, None)

		# this seems to be vaguely related, but not always there?
		self.extra_pc_zero = name_type_map['Uint64'](self.context, 0, None)
		self.anoth_pad_2 = name_type_map['PadAlign'](self.context, 16, self.ref)
		self.ref_3 = name_type_map['Empty'](self.context, 0, None)
		self.repeats = Array(self.context, 0, None, (0,), name_type_map['Repeat'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ref', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'floatsa', Array, (0, None, (None, None,), name_type_map['Float']), (False, None), (None, None)
		yield 'pad_2', name_type_map['SmartPadding'], (0, None), (False, None), (None, None)
		yield 'frame_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'ori_bone_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'pos_bone_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'scl_bone_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'zeros_18', Array, (0, None, (18,), name_type_map['Uint']), (False, None), (None, None)
		yield 'count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'quantisation_level', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'ref_2', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'some_indices', Array, (0, None, (None,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'flag_0', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'flag_1', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'flag_2', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'flag_3', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'anoth_pad', name_type_map['PadAlign'], (4, None), (False, None), (None, None)
		yield 'floatsb', name_type_map['FloatsGrabber'], (0, None), (False, None), (None, None)
		yield 'extra_pc_zero', name_type_map['Uint64'], (0, None), (False, None), (lambda context: context.version <= 257, None)
		yield 'anoth_pad_2', name_type_map['PadAlign'], (16, None), (False, None), (None, None)
		yield 'ref_3', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'repeats', Array, (0, None, (None,), name_type_map['Repeat']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None)
		yield 'floatsa', Array, (0, None, (instance.arg.frame_count, instance.arg.float_count,), name_type_map['Float']), (False, None)
		yield 'pad_2', name_type_map['SmartPadding'], (0, None), (False, None)
		yield 'frame_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'ori_bone_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'pos_bone_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'scl_bone_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'zeros_18', Array, (0, None, (18,), name_type_map['Uint']), (False, None)
		yield 'count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'quantisation_level', name_type_map['Ushort'], (0, None), (False, None)
		yield 'ref_2', name_type_map['Empty'], (0, None), (False, None)
		yield 'some_indices', Array, (0, None, (instance.pos_bone_count,), name_type_map['Ubyte']), (False, None)
		yield 'flag_0', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'flag_1', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'flag_2', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'flag_3', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'anoth_pad', name_type_map['PadAlign'], (4, instance.ref_2), (False, None)
		yield 'floatsb', name_type_map['FloatsGrabber'], (0, None), (False, None)
		if instance.context.version <= 257:
			yield 'extra_pc_zero', name_type_map['Uint64'], (0, None), (False, None)
		yield 'anoth_pad_2', name_type_map['PadAlign'], (16, instance.ref), (False, None)
		yield 'ref_3', name_type_map['Empty'], (0, None), (False, None)
		yield 'repeats', Array, (0, None, (instance.count,), name_type_map['Repeat']), (False, None)
