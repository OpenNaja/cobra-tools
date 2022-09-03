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
from generated.formats.ms2.compounds.Bone import Bone
from generated.formats.ms2.compounds.JointData import JointData
from generated.formats.ms2.compounds.Matrix44 import Matrix44
from generated.formats.ms2.compounds.MinusPadding import MinusPadding
from generated.formats.ms2.compounds.Struct7 import Struct7
from generated.formats.ms2.compounds.ZerosPadding import ZerosPadding


class BoneInfo(BaseStruct):

	"""
	# 858 in DLA c_cl_thread_.ms2
	"""

	__name__ = 'BoneInfo'

	_import_path = 'generated.formats.ms2.compounds.BoneInfo'

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
		self.zeros = Array((0,), Uint64, self.context, 0, None)
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
		self.name_indices = Array((0,), Ushort, self.context, 0, None)
		self.inventory_name_indices = Array((0,), Ushort, self.context, 0, None)
		self.name_padding = Array((0,), Byte, self.context, 0, None)

		# used for skinning
		self.inverse_bind_matrices = Array((0,), Matrix44, self.context, 0, None)
		self.bones = Array((0,), Bone, self.context, 0, None)

		# 255 = root, index in this list is the current bone index, value is the bone's parent index
		self.parents = Array((0,), Ubyte, self.context, 0, None)

		# zeros
		self.parents_padding = Array((0,), Byte, self.context, 0, None)

		# enumerates all bone indices, 4 may be flags

		# enumerates all bone indices
		self.enumeration = Array((0,), Ubyte, self.context, 0, None)

		# zeros
		self.inventory_datas = Array((0,), Byte, self.context, 0, None)

		# -1s and 0s

		# zeros
		self.weirdness = Array((0,), Short, self.context, 0, None)

		# zeros
		self.inventory_datas_2 = Array((0,), Int, self.context, 0, None)

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

	def set_defaults(self):
		super().set_defaults()
		self.name_count = 0
		self.z_0 = 0
		self.inv_names_count = 0
		if self.context.version >= 32:
			self.knownff = 0
			self.zero_0 = 0
			self.unknown_0_c = 0
		self.unk_count = 0
		self.bind_matrix_count = 0
		self.zeros = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		self.inv_data_count = 0
		self.bone_count = 0
		self.unknown_40 = 0
		self.parents_count = 0
		if (self.context.version == 7) or ((self.context.version == 13) or (((self.context.version == 48) or (self.context.version == 50)) or (self.context.version == 51))):
			self.extra_zero = 0
		self.enum_count = 0
		self.unknown_58 = 0
		self.one = 0
		self.zeros_count = 0
		if self.context.version == 32:
			self.unk_pc_count = 0
		self.count_7 = 0
		self.joint_count = 0
		self.unk_78_count = 0
		if self.context.version <= 13:
			self.unk_extra = 0
		if (self.context.version == 47) or (self.context.version == 39):
			self.unk_extra_jwe = 0
		if not (self.context.version < 47):
			self.name_indices = numpy.zeros((self.name_count,), dtype=numpy.dtype('uint32'))
		if self.context.version < 47:
			self.name_indices = numpy.zeros((self.name_count,), dtype=numpy.dtype('uint16'))
			self.inventory_name_indices = numpy.zeros((self.inv_names_count,), dtype=numpy.dtype('uint16'))
		if not (self.context.version < 47):
			self.name_padding = numpy.zeros(((16 - (((self.name_count + self.inv_names_count) * 4) % 16)) % 16,), dtype=numpy.dtype('int8'))
		if self.context.version < 47:
			self.name_padding = numpy.zeros(((16 - (((self.name_count + self.inv_names_count) * 2) % 16)) % 16,), dtype=numpy.dtype('int8'))
		self.inverse_bind_matrices = Array((self.bind_matrix_count,), Matrix44, self.context, 0, None)
		self.bones = Array((self.bone_count,), Bone, self.context, 0, None)
		self.parents = numpy.zeros((self.parents_count,), dtype=numpy.dtype('uint8'))
		if self.context.version >= 32:
			self.parents_padding = numpy.zeros(((8 - (self.parents_count % 8)) % 8,), dtype=numpy.dtype('int8'))
		if self.context.version >= 32 and self.one:
			self.enumeration = numpy.zeros((self.enum_count, 2,), dtype=numpy.dtype('uint32'))
		if self.context.version <= 13 and self.one:
			self.enumeration = numpy.zeros((self.enum_count,), dtype=numpy.dtype('uint8'))
		if self.context.version == 7:
			self.inventory_datas = numpy.zeros((self.inv_data_count, 6,), dtype=numpy.dtype('int8'))
			self.weirdness = numpy.zeros((8,), dtype=numpy.dtype('int16'))
		if self.context.version == 13:
			self.weirdness = numpy.zeros((10,), dtype=numpy.dtype('int16'))
		if self.context.version == 7:
			self.inventory_datas_2 = numpy.zeros((self.inv_data_count, 2,), dtype=numpy.dtype('int32'))
		if not (self.context.version < 47) and self.zeros_count:
			self.zeros_padding = ZerosPadding(self.context, self.zeros_count, None)
		if self.context.version >= 47 and self.zeros_count:
			self.minus_padding = MinusPadding(self.context, self.zeros_count, None)
		if self.count_7:
			self.struct_7 = Struct7(self.context, 0, None)
		if self.joint_count:
			self.joints = JointData(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.name_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.z_0 = Ushort.from_stream(stream, instance.context, 0, None)
		instance.inv_names_count = Ushort.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 32:
			instance.knownff = Short.from_stream(stream, instance.context, 0, None)
			instance.zero_0 = Short.from_stream(stream, instance.context, 0, None)
			instance.unknown_0_c = Uint.from_stream(stream, instance.context, 0, None)
		instance.unk_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.bind_matrix_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.zeros = Array.from_stream(stream, instance.context, 0, None, (2,), Uint64)
		instance.inv_data_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.bone_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.unknown_40 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.parents_count = Uint64.from_stream(stream, instance.context, 0, None)
		if (instance.context.version == 7) or ((instance.context.version == 13) or (((instance.context.version == 48) or (instance.context.version == 50)) or (instance.context.version == 51))):
			instance.extra_zero = Uint64.from_stream(stream, instance.context, 0, None)
		instance.enum_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.unknown_58 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.one = Uint64.from_stream(stream, instance.context, 0, None)
		instance.zeros_count = Uint64.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 32:
			instance.unk_pc_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.count_7 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.joint_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.unk_78_count = Uint64.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 13:
			instance.unk_extra = Uint64.from_stream(stream, instance.context, 0, None)
		if (instance.context.version == 47) or (instance.context.version == 39):
			instance.unk_extra_jwe = Uint64.from_stream(stream, instance.context, 0, None)
		if not (instance.context.version < 47):
			instance.name_indices = Array.from_stream(stream, instance.context, 0, None, (instance.name_count,), Uint)
		if instance.context.version < 47:
			instance.name_indices = Array.from_stream(stream, instance.context, 0, None, (instance.name_count,), Ushort)
			instance.inventory_name_indices = Array.from_stream(stream, instance.context, 0, None, (instance.inv_names_count,), Ushort)
		if not (instance.context.version < 47):
			instance.name_padding = Array.from_stream(stream, instance.context, 0, None, ((16 - (((instance.name_count + instance.inv_names_count) * 4) % 16)) % 16,), Byte)
		if instance.context.version < 47:
			instance.name_padding = Array.from_stream(stream, instance.context, 0, None, ((16 - (((instance.name_count + instance.inv_names_count) * 2) % 16)) % 16,), Byte)
		instance.inverse_bind_matrices = Array.from_stream(stream, instance.context, 0, None, (instance.bind_matrix_count,), Matrix44)
		instance.bones = Array.from_stream(stream, instance.context, 0, None, (instance.bone_count,), Bone)
		instance.parents = Array.from_stream(stream, instance.context, 0, None, (instance.parents_count,), Ubyte)
		if instance.context.version >= 32:
			instance.parents_padding = Array.from_stream(stream, instance.context, 0, None, ((8 - (instance.parents_count % 8)) % 8,), Byte)
		if instance.context.version >= 32 and instance.one:
			instance.enumeration = Array.from_stream(stream, instance.context, 0, None, (instance.enum_count, 2,), Uint)
		if instance.context.version <= 13 and instance.one:
			instance.enumeration = Array.from_stream(stream, instance.context, 0, None, (instance.enum_count,), Ubyte)
		if instance.context.version == 7:
			instance.inventory_datas = Array.from_stream(stream, instance.context, 0, None, (instance.inv_data_count, 6,), Byte)
			instance.weirdness = Array.from_stream(stream, instance.context, 0, None, (8,), Short)
		if instance.context.version == 13:
			instance.weirdness = Array.from_stream(stream, instance.context, 0, None, (10,), Short)
		if instance.context.version == 7:
			instance.inventory_datas_2 = Array.from_stream(stream, instance.context, 0, None, (instance.inv_data_count, 2,), Int)
		if not (instance.context.version < 47) and instance.zeros_count:
			instance.zeros_padding = ZerosPadding.from_stream(stream, instance.context, instance.zeros_count, None)
		if instance.context.version >= 47 and instance.zeros_count:
			instance.minus_padding = MinusPadding.from_stream(stream, instance.context, instance.zeros_count, None)
		if instance.count_7:
			instance.struct_7 = Struct7.from_stream(stream, instance.context, 0, None)
		if instance.joint_count:
			instance.joints = JointData.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.name_count)
		Ushort.to_stream(stream, instance.z_0)
		Ushort.to_stream(stream, instance.inv_names_count)
		if instance.context.version >= 32:
			Short.to_stream(stream, instance.knownff)
			Short.to_stream(stream, instance.zero_0)
			Uint.to_stream(stream, instance.unknown_0_c)
		Uint64.to_stream(stream, instance.unk_count)
		Uint64.to_stream(stream, instance.bind_matrix_count)
		Array.to_stream(stream, instance.zeros, (2,), Uint64, instance.context, 0, None)
		Uint64.to_stream(stream, instance.inv_data_count)
		Uint64.to_stream(stream, instance.bone_count)
		Uint64.to_stream(stream, instance.unknown_40)
		Uint64.to_stream(stream, instance.parents_count)
		if (instance.context.version == 7) or ((instance.context.version == 13) or (((instance.context.version == 48) or (instance.context.version == 50)) or (instance.context.version == 51))):
			Uint64.to_stream(stream, instance.extra_zero)
		Uint64.to_stream(stream, instance.enum_count)
		Uint64.to_stream(stream, instance.unknown_58)
		Uint64.to_stream(stream, instance.one)
		Uint64.to_stream(stream, instance.zeros_count)
		if instance.context.version == 32:
			Uint64.to_stream(stream, instance.unk_pc_count)
		Uint64.to_stream(stream, instance.count_7)
		Uint64.to_stream(stream, instance.joint_count)
		Uint64.to_stream(stream, instance.unk_78_count)
		if instance.context.version <= 13:
			Uint64.to_stream(stream, instance.unk_extra)
		if (instance.context.version == 47) or (instance.context.version == 39):
			Uint64.to_stream(stream, instance.unk_extra_jwe)
		if not (instance.context.version < 47):
			Array.to_stream(stream, instance.name_indices, (instance.name_count,), Uint, instance.context, 0, None)
		if instance.context.version < 47:
			Array.to_stream(stream, instance.name_indices, (instance.name_count,), Ushort, instance.context, 0, None)
			Array.to_stream(stream, instance.inventory_name_indices, (instance.inv_names_count,), Ushort, instance.context, 0, None)
		if not (instance.context.version < 47):
			instance.name_padding.resize(((16 - (((instance.name_count + instance.inv_names_count) * 4) % 16)) % 16,))
			Array.to_stream(stream, instance.name_padding, ((16 - (((instance.name_count + instance.inv_names_count) * 4) % 16)) % 16,), Byte, instance.context, 0, None)
		if instance.context.version < 47:
			instance.name_padding.resize(((16 - (((instance.name_count + instance.inv_names_count) * 2) % 16)) % 16,))
			Array.to_stream(stream, instance.name_padding, ((16 - (((instance.name_count + instance.inv_names_count) * 2) % 16)) % 16,), Byte, instance.context, 0, None)
		Array.to_stream(stream, instance.inverse_bind_matrices, (instance.bind_matrix_count,), Matrix44, instance.context, 0, None)
		Array.to_stream(stream, instance.bones, (instance.bone_count,), Bone, instance.context, 0, None)
		Array.to_stream(stream, instance.parents, (instance.parents_count,), Ubyte, instance.context, 0, None)
		if instance.context.version >= 32:
			instance.parents_padding.resize(((8 - (instance.parents_count % 8)) % 8,))
			Array.to_stream(stream, instance.parents_padding, ((8 - (instance.parents_count % 8)) % 8,), Byte, instance.context, 0, None)
		if instance.context.version >= 32 and instance.one:
			Array.to_stream(stream, instance.enumeration, (instance.enum_count, 2,), Uint, instance.context, 0, None)
		if instance.context.version <= 13 and instance.one:
			Array.to_stream(stream, instance.enumeration, (instance.enum_count,), Ubyte, instance.context, 0, None)
		if instance.context.version == 7:
			Array.to_stream(stream, instance.inventory_datas, (instance.inv_data_count, 6,), Byte, instance.context, 0, None)
			Array.to_stream(stream, instance.weirdness, (8,), Short, instance.context, 0, None)
		if instance.context.version == 13:
			Array.to_stream(stream, instance.weirdness, (10,), Short, instance.context, 0, None)
		if instance.context.version == 7:
			Array.to_stream(stream, instance.inventory_datas_2, (instance.inv_data_count, 2,), Int, instance.context, 0, None)
		if not (instance.context.version < 47) and instance.zeros_count:
			ZerosPadding.to_stream(stream, instance.zeros_padding)
		if instance.context.version >= 47 and instance.zeros_count:
			MinusPadding.to_stream(stream, instance.minus_padding)
		if instance.count_7:
			Struct7.to_stream(stream, instance.struct_7)
		if instance.joint_count:
			JointData.to_stream(stream, instance.joints)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'name_count', Uint, (0, None), (False, None)
		yield 'z_0', Ushort, (0, None), (False, None)
		yield 'inv_names_count', Ushort, (0, None), (False, None)
		if instance.context.version >= 32:
			yield 'knownff', Short, (0, None), (False, None)
			yield 'zero_0', Short, (0, None), (False, None)
			yield 'unknown_0_c', Uint, (0, None), (False, None)
		yield 'unk_count', Uint64, (0, None), (False, None)
		yield 'bind_matrix_count', Uint64, (0, None), (False, None)
		yield 'zeros', Array, ((2,), Uint64, 0, None), (False, None)
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
		if not (instance.context.version < 47):
			yield 'name_indices', Array, ((instance.name_count,), Uint, 0, None), (False, None)
		if instance.context.version < 47:
			yield 'name_indices', Array, ((instance.name_count,), Ushort, 0, None), (False, None)
			yield 'inventory_name_indices', Array, ((instance.inv_names_count,), Ushort, 0, None), (False, None)
		if not (instance.context.version < 47):
			yield 'name_padding', Array, (((16 - (((instance.name_count + instance.inv_names_count) * 4) % 16)) % 16,), Byte, 0, None), (False, None)
		if instance.context.version < 47:
			yield 'name_padding', Array, (((16 - (((instance.name_count + instance.inv_names_count) * 2) % 16)) % 16,), Byte, 0, None), (False, None)
		yield 'inverse_bind_matrices', Array, ((instance.bind_matrix_count,), Matrix44, 0, None), (False, None)
		yield 'bones', Array, ((instance.bone_count,), Bone, 0, None), (False, None)
		yield 'parents', Array, ((instance.parents_count,), Ubyte, 0, None), (False, None)
		if instance.context.version >= 32:
			yield 'parents_padding', Array, (((8 - (instance.parents_count % 8)) % 8,), Byte, 0, None), (False, None)
		if instance.context.version >= 32 and instance.one:
			yield 'enumeration', Array, ((instance.enum_count, 2,), Uint, 0, None), (False, None)
		if instance.context.version <= 13 and instance.one:
			yield 'enumeration', Array, ((instance.enum_count,), Ubyte, 0, None), (False, None)
		if instance.context.version == 7:
			yield 'inventory_datas', Array, ((instance.inv_data_count, 6,), Byte, 0, None), (False, None)
			yield 'weirdness', Array, ((8,), Short, 0, None), (False, None)
		if instance.context.version == 13:
			yield 'weirdness', Array, ((10,), Short, 0, None), (False, None)
		if instance.context.version == 7:
			yield 'inventory_datas_2', Array, ((instance.inv_data_count, 2,), Int, 0, None), (False, None)
		if not (instance.context.version < 47) and instance.zeros_count:
			yield 'zeros_padding', ZerosPadding, (instance.zeros_count, None), (False, None)
		if instance.context.version >= 47 and instance.zeros_count:
			yield 'minus_padding', MinusPadding, (instance.zeros_count, None), (False, None)
		if instance.count_7:
			yield 'struct_7', Struct7, (0, None), (False, None)
		if instance.joint_count:
			yield 'joints', JointData, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'BoneInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* name_count = {self.fmt_member(self.name_count, indent+1)}'
		s += f'\n	* z_0 = {self.fmt_member(self.z_0, indent+1)}'
		s += f'\n	* inv_names_count = {self.fmt_member(self.inv_names_count, indent+1)}'
		s += f'\n	* knownff = {self.fmt_member(self.knownff, indent+1)}'
		s += f'\n	* zero_0 = {self.fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* unknown_0_c = {self.fmt_member(self.unknown_0_c, indent+1)}'
		s += f'\n	* unk_count = {self.fmt_member(self.unk_count, indent+1)}'
		s += f'\n	* bind_matrix_count = {self.fmt_member(self.bind_matrix_count, indent+1)}'
		s += f'\n	* zeros = {self.fmt_member(self.zeros, indent+1)}'
		s += f'\n	* inv_data_count = {self.fmt_member(self.inv_data_count, indent+1)}'
		s += f'\n	* bone_count = {self.fmt_member(self.bone_count, indent+1)}'
		s += f'\n	* unknown_40 = {self.fmt_member(self.unknown_40, indent+1)}'
		s += f'\n	* parents_count = {self.fmt_member(self.parents_count, indent+1)}'
		s += f'\n	* extra_zero = {self.fmt_member(self.extra_zero, indent+1)}'
		s += f'\n	* enum_count = {self.fmt_member(self.enum_count, indent+1)}'
		s += f'\n	* unknown_58 = {self.fmt_member(self.unknown_58, indent+1)}'
		s += f'\n	* one = {self.fmt_member(self.one, indent+1)}'
		s += f'\n	* zeros_count = {self.fmt_member(self.zeros_count, indent+1)}'
		s += f'\n	* unk_pc_count = {self.fmt_member(self.unk_pc_count, indent+1)}'
		s += f'\n	* count_7 = {self.fmt_member(self.count_7, indent+1)}'
		s += f'\n	* joint_count = {self.fmt_member(self.joint_count, indent+1)}'
		s += f'\n	* unk_78_count = {self.fmt_member(self.unk_78_count, indent+1)}'
		s += f'\n	* unk_extra = {self.fmt_member(self.unk_extra, indent+1)}'
		s += f'\n	* unk_extra_jwe = {self.fmt_member(self.unk_extra_jwe, indent+1)}'
		s += f'\n	* name_indices = {self.fmt_member(self.name_indices, indent+1)}'
		s += f'\n	* inventory_name_indices = {self.fmt_member(self.inventory_name_indices, indent+1)}'
		s += f'\n	* name_padding = {self.fmt_member(self.name_padding, indent+1)}'
		s += f'\n	* inverse_bind_matrices = {self.fmt_member(self.inverse_bind_matrices, indent+1)}'
		s += f'\n	* bones = {self.fmt_member(self.bones, indent+1)}'
		s += f'\n	* parents = {self.fmt_member(self.parents, indent+1)}'
		s += f'\n	* parents_padding = {self.fmt_member(self.parents_padding, indent+1)}'
		s += f'\n	* enumeration = {self.fmt_member(self.enumeration, indent+1)}'
		s += f'\n	* inventory_datas = {self.fmt_member(self.inventory_datas, indent+1)}'
		s += f'\n	* weirdness = {self.fmt_member(self.weirdness, indent+1)}'
		s += f'\n	* inventory_datas_2 = {self.fmt_member(self.inventory_datas_2, indent+1)}'
		s += f'\n	* zeros_padding = {self.fmt_member(self.zeros_padding, indent+1)}'
		s += f'\n	* minus_padding = {self.fmt_member(self.minus_padding, indent+1)}'
		s += f'\n	* struct_7 = {self.fmt_member(self.struct_7, indent+1)}'
		s += f'\n	* joints = {self.fmt_member(self.joints, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
