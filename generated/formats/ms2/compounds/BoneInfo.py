import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Int
from generated.formats.base.basic import Short
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.base.compounds.PadAlign import PadAlign
from generated.formats.ms2.compounds.Bone import Bone
from generated.formats.ms2.compounds.JointData import JointData
from generated.formats.ms2.compounds.Matrix44 import Matrix44
from generated.formats.ms2.compounds.MinusPadding import MinusPadding
from generated.formats.ms2.compounds.Struct7 import Struct7
from generated.formats.ms2.compounds.ZerosPadding import ZerosPadding
from generated.formats.ovl_base.compounds.Empty import Empty


class BoneInfo(BaseStruct):

	"""
	# 858 in DLA c_cl_thread_.ms2
	"""

	__name__ = 'BoneInfo'

	_import_key = 'ms2.compounds.BoneInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# counts the names
		self.name_count = 0

		# ?
		self.z_0 = 0

		# ?
		self.inv_names_count = 0

		# this is always FFFF for now
		self.knownff = 0

		# this is always 0000 for now
		self.zero_0 = 0
		self.unknown_0_c = 0

		# almost always 4, 1 for male african lion
		self.unk_count = 0

		# seems to match bone count
		self.bind_matrix_count = 0
		self.zeros = Array(self.context, 0, None, (0,), Uint64)
		self.inv_data_count = 0
		self.bone_count = 0
		self.unknown_40 = 0
		self.parents_count = 0

		# not PC, JWE1
		self.extra_zero = 0
		self.enum_count = 0

		# usually zero
		self.unknown_58 = 0

		# always 1
		self.one = 0

		# this counts the weird padding at the end, usually == bone count, 0 in PZ aardvark
		self.zeros_count = 0

		# matches the other count on dino entertainer, but count7 is not present
		self.unk_pc_count = 0

		# index count 7
		self.count_7 = 0

		# joint count
		self.joint_count = 0

		# zero
		self.unk_78_count = 0

		# zero
		self.unk_extra = 0

		# zero
		self.unk_extra_jwe = 0
		self.names_ref = Empty(self.context, 0, None)
		self.name_indices = Array(self.context, 0, None, (0,), Ushort)
		self.inventory_name_indices = Array(self.context, 0, None, (0,), Ushort)

		# align to 16 bytes
		self.name_padding = PadAlign(self.context, 16, self.names_ref)

		# used for skinning
		self.inverse_bind_matrices = Array(self.context, 0, None, (0,), Matrix44)
		self.bones = Array(self.context, 0, None, (0,), Bone)

		# 255 = root, index in this list is the current bone index, value is the bone's parent index
		self.parents = Array(self.context, 0, None, (0,), Ubyte)

		# align to 8 bytes
		self.parents_padding = PadAlign(self.context, 8, self.names_ref)

		# enumerates all bone indices, 4 may be flags

		# enumerates all bone indices
		self.enumeration = Array(self.context, 0, None, (0,), Ubyte)

		# zeros
		self.inventory_datas = Array(self.context, 0, None, (0,), Byte)

		# -1s and 0s

		# zeros
		self.weirdness = Array(self.context, 0, None, (0,), Short)

		# zeros
		self.inventory_datas_2 = Array(self.context, 0, None, (0,), Int)

		# weird zeros
		self.zeros_padding = ZerosPadding(self.context, self.zeros_count, None)

		# weird -1s
		self.minus_padding = MinusPadding(self.context, self.zeros_count, None)

		# ragdoll links?
		self.struct_7 = Struct7(self.context, 0, None)

		# joints
		self.joints = JointData(self.context, 0, None)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('name_count', Uint, (0, None), (False, None), None),
		('z_0', Ushort, (0, None), (False, None), None),
		('inv_names_count', Ushort, (0, None), (False, None), None),
		('knownff', Short, (0, None), (False, None), True),
		('zero_0', Short, (0, None), (False, None), True),
		('unknown_0_c', Uint, (0, None), (False, None), True),
		('unk_count', Uint64, (0, None), (False, None), None),
		('bind_matrix_count', Uint64, (0, None), (False, None), None),
		('zeros', Array, (0, None, (2,), Uint64), (False, None), None),
		('inv_data_count', Uint64, (0, None), (False, None), None),
		('bone_count', Uint64, (0, None), (False, None), None),
		('unknown_40', Uint64, (0, None), (False, None), None),
		('parents_count', Uint64, (0, None), (False, None), None),
		('extra_zero', Uint64, (0, None), (False, None), True),
		('enum_count', Uint64, (0, None), (False, None), None),
		('unknown_58', Uint64, (0, None), (False, None), None),
		('one', Uint64, (0, None), (False, None), None),
		('zeros_count', Uint64, (0, None), (False, None), None),
		('unk_pc_count', Uint64, (0, None), (False, None), True),
		('count_7', Uint64, (0, None), (False, None), None),
		('joint_count', Uint64, (0, None), (False, None), None),
		('unk_78_count', Uint64, (0, None), (False, None), None),
		('unk_extra', Uint64, (0, None), (False, None), True),
		('unk_extra_jwe', Uint64, (0, None), (False, None), True),
		('names_ref', Empty, (0, None), (False, None), None),
		('name_indices', Array, (0, None, (None,), Uint), (False, None), True),
		('name_indices', Array, (0, None, (None,), Ushort), (False, None), True),
		('inventory_name_indices', Array, (0, None, (None,), Ushort), (False, None), True),
		('name_padding', PadAlign, (16, None), (False, None), None),
		('inverse_bind_matrices', Array, (0, None, (None,), Matrix44), (False, None), None),
		('bones', Array, (0, None, (None,), Bone), (False, None), None),
		('parents', Array, (0, None, (None,), Ubyte), (False, None), None),
		('parents_padding', PadAlign, (8, None), (False, None), True),
		('enumeration', Array, (0, None, (None, 2,), Uint), (False, None), True),
		('enumeration', Array, (0, None, (None,), Ubyte), (False, None), True),
		('inventory_datas', Array, (0, None, (None, 6,), Byte), (False, None), True),
		('weirdness', Array, (0, None, (8,), Short), (False, None), True),
		('weirdness', Array, (0, None, (10,), Short), (False, None), True),
		('inventory_datas_2', Array, (0, None, (None, 2,), Int), (False, None), True),
		('zeros_padding', ZerosPadding, (None, None), (False, None), True),
		('minus_padding', MinusPadding, (None, None), (False, None), True),
		('struct_7', Struct7, (0, None), (False, None), True),
		('joints', JointData, (0, None), (False, None), True),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'name_count', Uint, (0, None), (False, None)
		yield 'z_0', Ushort, (0, None), (False, None)
		yield 'inv_names_count', Ushort, (0, None), (False, None)
		if instance.context.version >= 32:
			yield 'knownff', Short, (0, None), (False, None)
			yield 'zero_0', Short, (0, None), (False, None)
			yield 'unknown_0_c', Uint, (0, None), (False, None)
		yield 'unk_count', Uint64, (0, None), (False, None)
		yield 'bind_matrix_count', Uint64, (0, None), (False, None)
		yield 'zeros', Array, (0, None, (2,), Uint64), (False, None)
		yield 'inv_data_count', Uint64, (0, None), (False, None)
		yield 'bone_count', Uint64, (0, None), (False, None)
		yield 'unknown_40', Uint64, (0, None), (False, None)
		yield 'parents_count', Uint64, (0, None), (False, None)
		if (instance.context.version == 7) or ((instance.context.version == 13) or (((instance.context.version == 48) or (instance.context.version == 50)) or (instance.context.version == 51))):
			yield 'extra_zero', Uint64, (0, None), (False, None)
		yield 'enum_count', Uint64, (0, None), (False, None)
		yield 'unknown_58', Uint64, (0, None), (False, None)
		yield 'one', Uint64, (0, None), (False, None)
		yield 'zeros_count', Uint64, (0, None), (False, None)
		if instance.context.version == 32:
			yield 'unk_pc_count', Uint64, (0, None), (False, None)
		yield 'count_7', Uint64, (0, None), (False, None)
		yield 'joint_count', Uint64, (0, None), (False, None)
		yield 'unk_78_count', Uint64, (0, None), (False, None)
		if instance.context.version <= 13:
			yield 'unk_extra', Uint64, (0, None), (False, None)
		if (instance.context.version == 47) or (instance.context.version == 39):
			yield 'unk_extra_jwe', Uint64, (0, None), (False, None)
		yield 'names_ref', Empty, (0, None), (False, None)
		if not (instance.context.version < 47):
			yield 'name_indices', Array, (0, None, (instance.name_count,), Uint), (False, None)
		if instance.context.version < 47:
			yield 'name_indices', Array, (0, None, (instance.name_count,), Ushort), (False, None)
			yield 'inventory_name_indices', Array, (0, None, (instance.inv_names_count,), Ushort), (False, None)
		yield 'name_padding', PadAlign, (16, instance.names_ref), (False, None)
		yield 'inverse_bind_matrices', Array, (0, None, (instance.bind_matrix_count,), Matrix44), (False, None)
		yield 'bones', Array, (0, None, (instance.bone_count,), Bone), (False, None)
		yield 'parents', Array, (0, None, (instance.parents_count,), Ubyte), (False, None)
		if instance.context.version >= 32:
			yield 'parents_padding', PadAlign, (8, instance.names_ref), (False, None)
		if instance.context.version >= 32 and instance.one:
			yield 'enumeration', Array, (0, None, (instance.enum_count, 2,), Uint), (False, None)
		if instance.context.version <= 13 and instance.one:
			yield 'enumeration', Array, (0, None, (instance.enum_count,), Ubyte), (False, None)
		if instance.context.version == 7:
			yield 'inventory_datas', Array, (0, None, (instance.inv_data_count, 6,), Byte), (False, None)
			yield 'weirdness', Array, (0, None, (8,), Short), (False, None)
		if instance.context.version == 13:
			yield 'weirdness', Array, (0, None, (10,), Short), (False, None)
		if instance.context.version == 7:
			yield 'inventory_datas_2', Array, (0, None, (instance.inv_data_count, 2,), Int), (False, None)
		if not (instance.context.version < 47) and instance.zeros_count:
			yield 'zeros_padding', ZerosPadding, (instance.zeros_count, None), (False, None)
		if instance.context.version >= 48 and instance.zeros_count:
			yield 'minus_padding', MinusPadding, (instance.zeros_count, None), (False, None)
		if instance.count_7:
			yield 'struct_7', Struct7, (0, None), (False, None)
		if instance.joint_count:
			yield 'joints', JointData, (0, None), (False, None)
