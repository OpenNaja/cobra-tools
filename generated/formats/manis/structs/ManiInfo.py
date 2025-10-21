from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class ManiInfo(BaseStruct):

	"""
	288 bytes for JWE (last member is not padded at end in stock) / PZ
	304 bytes for PC, ZTUAC (however the last 2 bytes are alignment, and not on the last member of the array)
	320 bytes for war
	304 bytes for PC2, possibly different manis dtype apparently use_ushort has moved
	"""

	__name__ = 'ManiInfo'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ref = name_type_map['Empty'](self.context, 0, None)
		self.duration = name_type_map['Float'](self.context, 0, None)
		self.frame_count = name_type_map['Uint'](self.context, 0, None)
		self.dtype = name_type_map['ManisDtypePC2'](self.context, 0, None)
		self.zeros_0 = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.extra_pc_1 = name_type_map['Ushort'](self.context, 0, None)
		self.pos_bone_count = name_type_map['Ushort'](self.context, 0, None)
		self.ori_bone_count = name_type_map['Ushort'](self.context, 0, None)
		self.scl_bone_count = name_type_map['Ushort'](self.context, 0, None)
		self.unk_count_0 = name_type_map['Ushort'](self.context, 0, None)
		self.unk_count_1 = name_type_map['Ushort'](self.context, 0, None)
		self.unk_count_2 = name_type_map['Ushort'](self.context, 0, None)
		self.extra_count = name_type_map['Ushort'](self.context, 0, None)
		self.float_count = name_type_map['Ushort'](self.context, 0, None)
		self.pos_bone_count_repeat = name_type_map['Ushort'](self.context, 0, None)
		self.ori_bone_count_repeat = name_type_map['Ushort'](self.context, 0, None)
		self.scl_bone_count_repeat = name_type_map['Ushort'](self.context, 0, None)
		self.unk_0 = name_type_map['Ushort'](self.context, 0, None)
		self.unk_1 = name_type_map['Ushort'](self.context, 0, None)
		self.root_pos_bone = name_type_map['BoneIndex'].from_value(255)
		self.root_ori_bone = name_type_map['BoneIndex'].from_value(255)

		# can include joints, such as in PZ water wheel count 5 vs ms2 2 bones, plus joints
		self.target_bone_count = name_type_map['Uint64'](self.context, 0, None)
		self.unk_2 = name_type_map['Ushort'](self.context, 0, None)
		self.unk_3 = name_type_map['Ushort'](self.context, 0, None)
		self.unk_4 = name_type_map['Ushort'](self.context, 0, None)
		self.unk_5 = name_type_map['Ushort'](self.context, 0, None)
		self.extra_zeros_pc = Array(self.context, 0, None, (0,), name_type_map['Ushort'])
		self.unk_5 = name_type_map['Ushort'](self.context, 0, None)
		self.unk_6 = name_type_map['Ushort'](self.context, 0, None)
		self.unk_7 = name_type_map['Ushort'](self.context, 0, None)
		self.unk_8 = name_type_map['Ushort'](self.context, 0, None)

		# 216 bytes
		self.pointers = Array(self.context, 0, None, (0,), name_type_map['Uint64'])
		self.extra_for_use_ushort = Array(self.context, 0, None, (0,), name_type_map['Ushort'])
		self.pos_bone_min = name_type_map['BoneIndex'](self.context, self.dtype, None)
		self.pos_bone_max = name_type_map['BoneIndex'](self.context, self.dtype, None)
		self.ori_bone_min = name_type_map['BoneIndex'](self.context, self.dtype, None)
		self.ori_bone_max = name_type_map['BoneIndex'](self.context, self.dtype, None)
		self.scl_bone_min = name_type_map['BoneIndex'](self.context, self.dtype, None)
		self.scl_bone_max = name_type_map['BoneIndex'](self.context, self.dtype, None)
		self.pos_bone_count_related = name_type_map['BoneIndex'](self.context, self.dtype, None)
		self.pos_bone_count_repeat = name_type_map['BoneIndex'](self.context, self.dtype, None)
		self.ori_bone_count_related = name_type_map['BoneIndex'](self.context, self.dtype, None)
		self.ori_bone_count_repeat = name_type_map['BoneIndex'](self.context, self.dtype, None)
		self.scl_bone_count_related = name_type_map['BoneIndex'](self.context, self.dtype, None)
		self.scl_bone_count_repeat = name_type_map['BoneIndex'](self.context, self.dtype, None)
		self.zero_0_end = name_type_map['Ushort'](self.context, 0, None)
		self.zero_1_end = name_type_map['Ushort'](self.context, 0, None)
		self.pad_2 = name_type_map['PadAlign'](self.context, 16, self.ref)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ref', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'duration', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'frame_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'dtype', name_type_map['ManisDtype'], (0, None), (False, None), (lambda context: not ((context.version == 262) and (context.mani_version == 282)), None)
		yield 'dtype', name_type_map['ManisDtypePC2'], (0, None), (False, None), (lambda context: (context.version == 262) and (context.mani_version == 282), None)
		yield 'zeros_0', Array, (0, None, (3,), name_type_map['Uint']), (False, None), (None, None)
		yield 'extra_pc_1', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version <= 258, None)
		yield 'pos_bone_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'ori_bone_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'scl_bone_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'unk_count_0', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'unk_count_1', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'unk_count_2', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'extra_count', name_type_map['Ushort'], (0, None), (False, None), (lambda context: (context.version == 262) and (context.mani_version == 282), None)
		yield 'float_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'pos_bone_count_repeat', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version <= 257, None)
		yield 'ori_bone_count_repeat', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version <= 257, None)
		yield 'scl_bone_count_repeat', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version <= 257, None)
		yield 'unk_0', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version <= 257, None)
		yield 'unk_1', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version <= 257, None)
		yield 'root_pos_bone', name_type_map['BoneIndex'], (None, None), (False, 255), (None, None)
		yield 'root_ori_bone', name_type_map['BoneIndex'], (None, None), (False, 255), (None, None)
		yield 'target_bone_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_2', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'unk_3', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'unk_4', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'unk_5', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version <= 257, None)
		yield 'extra_zeros_pc', Array, (0, None, (6,), name_type_map['Ushort']), (False, None), (lambda context: context.version <= 257, None)
		yield 'unk_5', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version >= 260, None)
		yield 'unk_6', name_type_map['Ushort'], (0, None), (False, None), (lambda context: (context.version == 262) and (context.mani_version == 282), None)
		yield 'unk_7', name_type_map['Ushort'], (0, None), (False, None), (lambda context: (context.version == 262) and (context.mani_version == 282), None)
		yield 'unk_8', name_type_map['Ushort'], (0, None), (False, None), (lambda context: (context.version == 262) and (context.mani_version == 282), None)
		yield 'pointers', Array, (0, None, (27,), name_type_map['Uint64']), (False, None), (None, None)
		yield 'extra_for_use_ushort', Array, (0, None, (7,), name_type_map['Ushort']), (False, None), (None, True)
		yield 'pos_bone_min', name_type_map['BoneIndex'], (None, None), (False, None), (None, None)
		yield 'pos_bone_max', name_type_map['BoneIndex'], (None, None), (False, None), (None, None)
		yield 'ori_bone_min', name_type_map['BoneIndex'], (None, None), (False, None), (None, None)
		yield 'ori_bone_max', name_type_map['BoneIndex'], (None, None), (False, None), (None, None)
		yield 'scl_bone_min', name_type_map['BoneIndex'], (None, None), (False, None), (None, None)
		yield 'scl_bone_max', name_type_map['BoneIndex'], (None, None), (False, None), (None, None)
		yield 'pos_bone_count_related', name_type_map['BoneIndex'], (None, None), (False, None), (lambda context: context.version >= 258, None)
		yield 'pos_bone_count_repeat', name_type_map['BoneIndex'], (None, None), (False, None), (lambda context: context.version >= 258, None)
		yield 'ori_bone_count_related', name_type_map['BoneIndex'], (None, None), (False, None), (lambda context: context.version >= 258, None)
		yield 'ori_bone_count_repeat', name_type_map['BoneIndex'], (None, None), (False, None), (lambda context: context.version >= 258, None)
		yield 'scl_bone_count_related', name_type_map['BoneIndex'], (None, None), (False, None), (lambda context: context.version >= 258, None)
		yield 'scl_bone_count_repeat', name_type_map['BoneIndex'], (None, None), (False, None), (lambda context: context.version >= 258, None)
		yield 'zero_0_end', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version >= 258, None)
		yield 'zero_1_end', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'pad_2', name_type_map['PadAlign'], (16, None), (False, None), (lambda context: context.version >= 258, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None)
		yield 'duration', name_type_map['Float'], (0, None), (False, None)
		yield 'frame_count', name_type_map['Uint'], (0, None), (False, None)
		if not ((instance.context.version == 262) and (instance.context.mani_version == 282)):
			yield 'dtype', name_type_map['ManisDtype'], (0, None), (False, None)
		if (instance.context.version == 262) and (instance.context.mani_version == 282):
			yield 'dtype', name_type_map['ManisDtypePC2'], (0, None), (False, None)
		yield 'zeros_0', Array, (0, None, (3,), name_type_map['Uint']), (False, None)
		if instance.context.version <= 258:
			yield 'extra_pc_1', name_type_map['Ushort'], (0, None), (False, None)
		yield 'pos_bone_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'ori_bone_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'scl_bone_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'unk_count_0', name_type_map['Ushort'], (0, None), (False, None)
		yield 'unk_count_1', name_type_map['Ushort'], (0, None), (False, None)
		yield 'unk_count_2', name_type_map['Ushort'], (0, None), (False, None)
		if (instance.context.version == 262) and (instance.context.mani_version == 282):
			yield 'extra_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'float_count', name_type_map['Ushort'], (0, None), (False, None)
		if instance.context.version <= 257:
			yield 'pos_bone_count_repeat', name_type_map['Ushort'], (0, None), (False, None)
			yield 'ori_bone_count_repeat', name_type_map['Ushort'], (0, None), (False, None)
			yield 'scl_bone_count_repeat', name_type_map['Ushort'], (0, None), (False, None)
			yield 'unk_0', name_type_map['Ushort'], (0, None), (False, None)
			yield 'unk_1', name_type_map['Ushort'], (0, None), (False, None)
		yield 'root_pos_bone', name_type_map['BoneIndex'], (instance.dtype, None), (False, 255)
		yield 'root_ori_bone', name_type_map['BoneIndex'], (instance.dtype, None), (False, 255)
		yield 'target_bone_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_2', name_type_map['Ushort'], (0, None), (False, None)
		yield 'unk_3', name_type_map['Ushort'], (0, None), (False, None)
		yield 'unk_4', name_type_map['Ushort'], (0, None), (False, None)
		if instance.context.version <= 257:
			yield 'unk_5', name_type_map['Ushort'], (0, None), (False, None)
			yield 'extra_zeros_pc', Array, (0, None, (6,), name_type_map['Ushort']), (False, None)
		if instance.context.version >= 260:
			yield 'unk_5', name_type_map['Ushort'], (0, None), (False, None)
		if (instance.context.version == 262) and (instance.context.mani_version == 282):
			yield 'unk_6', name_type_map['Ushort'], (0, None), (False, None)
			yield 'unk_7', name_type_map['Ushort'], (0, None), (False, None)
			yield 'unk_8', name_type_map['Ushort'], (0, None), (False, None)
		yield 'pointers', Array, (0, None, (27,), name_type_map['Uint64']), (False, None)
		if instance.dtype.use_ushort:
			yield 'extra_for_use_ushort', Array, (0, None, (7,), name_type_map['Ushort']), (False, None)
		yield 'pos_bone_min', name_type_map['BoneIndex'], (instance.dtype, None), (False, None)
		yield 'pos_bone_max', name_type_map['BoneIndex'], (instance.dtype, None), (False, None)
		yield 'ori_bone_min', name_type_map['BoneIndex'], (instance.dtype, None), (False, None)
		yield 'ori_bone_max', name_type_map['BoneIndex'], (instance.dtype, None), (False, None)
		yield 'scl_bone_min', name_type_map['BoneIndex'], (instance.dtype, None), (False, None)
		yield 'scl_bone_max', name_type_map['BoneIndex'], (instance.dtype, None), (False, None)
		if instance.context.version >= 258:
			yield 'pos_bone_count_related', name_type_map['BoneIndex'], (instance.dtype, None), (False, None)
			yield 'pos_bone_count_repeat', name_type_map['BoneIndex'], (instance.dtype, None), (False, None)
			yield 'ori_bone_count_related', name_type_map['BoneIndex'], (instance.dtype, None), (False, None)
			yield 'ori_bone_count_repeat', name_type_map['BoneIndex'], (instance.dtype, None), (False, None)
			yield 'scl_bone_count_related', name_type_map['BoneIndex'], (instance.dtype, None), (False, None)
			yield 'scl_bone_count_repeat', name_type_map['BoneIndex'], (instance.dtype, None), (False, None)
			yield 'zero_0_end', name_type_map['Ushort'], (0, None), (False, None)
		yield 'zero_1_end', name_type_map['Ushort'], (0, None), (False, None)
		if instance.context.version >= 258:
			yield 'pad_2', name_type_map['PadAlign'], (16, instance.ref), (False, None)
