import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.JointData import JointData
from generated.formats.ms2.compound.JweBone import JweBone
from generated.formats.ms2.compound.Matrix44 import Matrix44
from generated.formats.ms2.compound.MinusPadding import MinusPadding
from generated.formats.ms2.compound.PzBone import PzBone
from generated.formats.ms2.compound.SmartPadding import SmartPadding
from generated.formats.ms2.compound.Struct7 import Struct7
from generated.formats.ms2.compound.ZerosPadding import ZerosPadding


class Ms2BoneInfo:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# counts the names
		self.name_count = 0

		# this is always FFFF for now
		if not (self.context.version == 17):
			self.knownff = 0

		# this is always 0000 for now
		if not (self.context.version == 17):
			self.zero_0 = 0
		if not (self.context.version == 17):
			self.unknown_0_c = 0

		# almost always 4, 1 for male african lion
		self.unk_count = 0

		# seems to match bone count
		self.bind_matrix_count = 0
		self.zeros = numpy.zeros((3), dtype='uint64')

		# index count3
		self.bone_count = 0
		self.unknown_40 = 0

		# index count4
		self.bone_parents_count = 0

		# pZ only
		if ((self.context.user_version == 8340) or (self.context.user_version == 8724)) and (self.context.version >= 19):
			self.extra_uint_0 = 0

		# zero
		if self.context.version == 17:
			self.unk_zero_zt = 0

		# index count 5
		self.enum_count = 0

		# usually zero
		self.unknown_58 = 0

		# always 1
		self.one = 0

		# this counts the weird padding at the end, usually == bone count, 0 in PZ aardvark
		self.zeros_count = 0

		# index count 7
		self.count_7 = 0

		# zero
		if self.context.version < 19:
			self.unknownextra = 0

		# joint count
		self.joint_count = 0

		# unnk 78 count
		if not (self.context.version < 19):
			self.unk_78_count = 0

		# jwe only, everything is shifted a bit due to extra uint 0
		if (((self.context.user_version == 24724) or (self.context.user_version == 25108)) and (self.context.version == 19)) or (self.context.version < 19):
			self.unknown_88 = 0

		# index into ms2 string table for bones used here
		if not (self.context.version < 19):
			self.name_indices = numpy.zeros((self.name_count), dtype='uint')

		# index into ms2 string table for bones used here
		if self.context.version < 19:
			self.name_indices = numpy.zeros((self.name_count), dtype='ushort')

		# zeros. One index occupies 4 bytes; pad to multiples of 16 bytes.
		if not (self.context.version < 19):
			self.name_padding = numpy.zeros(((16 - ((self.name_count * 4) % 16)) % 16), dtype='byte')

		# zeros. One index occupies 4 bytes; pad to multiples of 16 bytes.
		if self.context.version < 19:
			self.name_padding = numpy.zeros(((16 - ((self.name_count * 2) % 16)) % 16), dtype='byte')

		# used for skinning
		self.inverse_bind_matrices = Array()

		# bones, rot first
		if ((self.context.user_version == 8340) or (self.context.user_version == 8724)) and (self.context.version >= 19):
			self.bones = Array()

		# bones, loc first
		if (((self.context.user_version == 24724) or (self.context.user_version == 25108)) and (self.context.version == 19)) or (self.context.version < 19):
			self.bones = Array()

		# 255 = root, index in this list is the current bone index, value is the bone's parent index
		self.bone_parents = numpy.zeros((self.bone_parents_count), dtype='ubyte')

		# zeros
		if not (self.context.version == 17):
			self.hier_1_padding = numpy.zeros(((8 - (self.bone_parents_count % 8)) % 8), dtype='byte')

		# enumerates all bone indices, 4 may be flags
		if not (self.context.version == 17) and self.one:
			self.enumeration = numpy.zeros((self.enum_count, 2), dtype='uint')

		# enumerates all bone indices, 4 may be flags
		if self.context.version == 17 and self.one:
			self.enumeration = numpy.zeros((self.enum_count), dtype='ubyte')

		# zeros
		if self.context.version == 17:
			self.zt_weirdness = numpy.zeros((10), dtype='ushort')

		# weird zeros
		if not (self.context.version < 19) and self.zeros_count:
			self.zeros_padding = ZerosPadding(context, self.zeros_count, None)

		# weird -1s
		if self.context.version < 19 and self.zeros_count:
			self.minus_padding = MinusPadding(context, self.zeros_count, None)

		# ragdoll links?
		if not (self.context.version < 19) and self.count_7:
			self.struct_7 = Struct7(context, None, None)
		if self.context.version == 18 and self.joint_count:
			self.weird_padding = SmartPadding(context, None, None)

		# joints
		if not (self.context.version == 17) and self.joint_count:
			self.joints = JointData(context, None, None)
		if self.context.version == 18 and not self.joint_count:
			self.weird_padding_2 = SmartPadding(context, None, None)

	def read(self, stream):

		self.io_start = stream.tell()
		self.name_count = stream.read_uint64()
		if not (self.context.version == 17):
			self.knownff = stream.read_short()
			self.zero_0 = stream.read_short()
		if not (self.context.version == 17):
			self.unknown_0_c = stream.read_uint()
		self.unk_count = stream.read_uint64()
		self.bind_matrix_count = stream.read_uint64()
		self.zeros = stream.read_uint64s((3))
		self.bone_count = stream.read_uint64()
		self.unknown_40 = stream.read_uint64()
		self.bone_parents_count = stream.read_uint64()
		if ((self.context.user_version == 8340) or (self.context.user_version == 8724)) and (self.context.version >= 19):
			self.extra_uint_0 = stream.read_uint64()
		if self.context.version == 17:
			self.unk_zero_zt = stream.read_uint64()
		self.enum_count = stream.read_uint64()
		self.unknown_58 = stream.read_uint64()
		self.one = stream.read_uint64()
		self.zeros_count = stream.read_uint64()
		self.count_7 = stream.read_uint64()
		if self.context.version < 19:
			self.unknownextra = stream.read_uint64()
		self.joint_count = stream.read_uint64()
		if not (self.context.version < 19):
			self.unk_78_count = stream.read_uint64()
		if (((self.context.user_version == 24724) or (self.context.user_version == 25108)) and (self.context.version == 19)) or (self.context.version < 19):
			self.unknown_88 = stream.read_uint64()
		if not (self.context.version < 19):
			self.name_indices = stream.read_uints((self.name_count))
		if self.context.version < 19:
			self.name_indices = stream.read_ushorts((self.name_count))
		if not (self.context.version < 19):
			self.name_padding = stream.read_bytes(((16 - ((self.name_count * 4) % 16)) % 16))
		if self.context.version < 19:
			self.name_padding = stream.read_bytes(((16 - ((self.name_count * 2) % 16)) % 16))
		self.inverse_bind_matrices.read(stream, Matrix44, self.bind_matrix_count, None)
		if ((self.context.user_version == 8340) or (self.context.user_version == 8724)) and (self.context.version >= 19):
			self.bones.read(stream, PzBone, self.bone_count, None)
		if (((self.context.user_version == 24724) or (self.context.user_version == 25108)) and (self.context.version == 19)) or (self.context.version < 19):
			self.bones.read(stream, JweBone, self.bone_count, None)
		self.bone_parents = stream.read_ubytes((self.bone_parents_count))
		if not (self.context.version == 17):
			self.hier_1_padding = stream.read_bytes(((8 - (self.bone_parents_count % 8)) % 8))
		if not (self.context.version == 17) and self.one:
			self.enumeration = stream.read_uints((self.enum_count, 2))
		if self.context.version == 17 and self.one:
			self.enumeration = stream.read_ubytes((self.enum_count))
		if self.context.version == 17:
			self.zt_weirdness = stream.read_ushorts((10))
		if not (self.context.version < 19) and self.zeros_count:
			self.zeros_padding = stream.read_type(ZerosPadding, (self.zeros_count, None))
		if self.context.version < 19 and self.zeros_count:
			self.minus_padding = stream.read_type(MinusPadding, (self.zeros_count, None))
		if not (self.context.version < 19) and self.count_7:
			self.struct_7 = stream.read_type(Struct7)
		if self.context.version == 18 and self.joint_count:
			self.weird_padding = stream.read_type(SmartPadding)
		if not (self.context.version == 17) and self.joint_count:
			self.joints = stream.read_type(JointData)
		if self.context.version == 18 and not self.joint_count:
			self.weird_padding_2 = stream.read_type(SmartPadding)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64(self.name_count)
		if not (self.context.version == 17):
			stream.write_short(self.knownff)
			stream.write_short(self.zero_0)
		if not (self.context.version == 17):
			stream.write_uint(self.unknown_0_c)
		stream.write_uint64(self.unk_count)
		stream.write_uint64(self.bind_matrix_count)
		stream.write_uint64s(self.zeros)
		stream.write_uint64(self.bone_count)
		stream.write_uint64(self.unknown_40)
		stream.write_uint64(self.bone_parents_count)
		if ((self.context.user_version == 8340) or (self.context.user_version == 8724)) and (self.context.version >= 19):
			stream.write_uint64(self.extra_uint_0)
		if self.context.version == 17:
			stream.write_uint64(self.unk_zero_zt)
		stream.write_uint64(self.enum_count)
		stream.write_uint64(self.unknown_58)
		stream.write_uint64(self.one)
		stream.write_uint64(self.zeros_count)
		stream.write_uint64(self.count_7)
		if self.context.version < 19:
			stream.write_uint64(self.unknownextra)
		stream.write_uint64(self.joint_count)
		if not (self.context.version < 19):
			stream.write_uint64(self.unk_78_count)
		if (((self.context.user_version == 24724) or (self.context.user_version == 25108)) and (self.context.version == 19)) or (self.context.version < 19):
			stream.write_uint64(self.unknown_88)
		if not (self.context.version < 19):
			stream.write_uints(self.name_indices)
		if self.context.version < 19:
			stream.write_ushorts(self.name_indices)
		if not (self.context.version < 19):
			self.name_padding.resize(((16 - ((self.name_count * 4) % 16)) % 16))
			stream.write_bytes(self.name_padding)
		if self.context.version < 19:
			self.name_padding.resize(((16 - ((self.name_count * 2) % 16)) % 16))
			stream.write_bytes(self.name_padding)
		self.inverse_bind_matrices.write(stream, Matrix44, self.bind_matrix_count, None)
		if ((self.context.user_version == 8340) or (self.context.user_version == 8724)) and (self.context.version >= 19):
			self.bones.write(stream, PzBone, self.bone_count, None)
		if (((self.context.user_version == 24724) or (self.context.user_version == 25108)) and (self.context.version == 19)) or (self.context.version < 19):
			self.bones.write(stream, JweBone, self.bone_count, None)
		stream.write_ubytes(self.bone_parents)
		if not (self.context.version == 17):
			self.hier_1_padding.resize(((8 - (self.bone_parents_count % 8)) % 8))
			stream.write_bytes(self.hier_1_padding)
		if not (self.context.version == 17) and self.one:
			stream.write_uints(self.enumeration)
		if self.context.version == 17 and self.one:
			stream.write_ubytes(self.enumeration)
		if self.context.version == 17:
			stream.write_ushorts(self.zt_weirdness)
		if not (self.context.version < 19) and self.zeros_count:
			stream.write_type(self.zeros_padding)
		if self.context.version < 19 and self.zeros_count:
			stream.write_type(self.minus_padding)
		if not (self.context.version < 19) and self.count_7:
			stream.write_type(self.struct_7)
		if self.context.version == 18 and self.joint_count:
			stream.write_type(self.weird_padding)
		if not (self.context.version == 17) and self.joint_count:
			stream.write_type(self.joints)
		if self.context.version == 18 and not self.joint_count:
			stream.write_type(self.weird_padding_2)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Ms2BoneInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* name_count = {self.name_count.__repr__()}'
		s += f'\n	* knownff = {self.knownff.__repr__()}'
		s += f'\n	* zero_0 = {self.zero_0.__repr__()}'
		s += f'\n	* unknown_0_c = {self.unknown_0_c.__repr__()}'
		s += f'\n	* unk_count = {self.unk_count.__repr__()}'
		s += f'\n	* bind_matrix_count = {self.bind_matrix_count.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* bone_count = {self.bone_count.__repr__()}'
		s += f'\n	* unknown_40 = {self.unknown_40.__repr__()}'
		s += f'\n	* bone_parents_count = {self.bone_parents_count.__repr__()}'
		s += f'\n	* extra_uint_0 = {self.extra_uint_0.__repr__()}'
		s += f'\n	* unk_zero_zt = {self.unk_zero_zt.__repr__()}'
		s += f'\n	* enum_count = {self.enum_count.__repr__()}'
		s += f'\n	* unknown_58 = {self.unknown_58.__repr__()}'
		s += f'\n	* one = {self.one.__repr__()}'
		s += f'\n	* zeros_count = {self.zeros_count.__repr__()}'
		s += f'\n	* count_7 = {self.count_7.__repr__()}'
		s += f'\n	* unknownextra = {self.unknownextra.__repr__()}'
		s += f'\n	* joint_count = {self.joint_count.__repr__()}'
		s += f'\n	* unk_78_count = {self.unk_78_count.__repr__()}'
		s += f'\n	* unknown_88 = {self.unknown_88.__repr__()}'
		s += f'\n	* name_indices = {self.name_indices.__repr__()}'
		s += f'\n	* name_padding = {self.name_padding.__repr__()}'
		s += f'\n	* inverse_bind_matrices = {self.inverse_bind_matrices.__repr__()}'
		s += f'\n	* bones = {self.bones.__repr__()}'
		s += f'\n	* bone_parents = {self.bone_parents.__repr__()}'
		s += f'\n	* hier_1_padding = {self.hier_1_padding.__repr__()}'
		s += f'\n	* enumeration = {self.enumeration.__repr__()}'
		s += f'\n	* zt_weirdness = {self.zt_weirdness.__repr__()}'
		s += f'\n	* zeros_padding = {self.zeros_padding.__repr__()}'
		s += f'\n	* minus_padding = {self.minus_padding.__repr__()}'
		s += f'\n	* struct_7 = {self.struct_7.__repr__()}'
		s += f'\n	* weird_padding = {self.weird_padding.__repr__()}'
		s += f'\n	* joints = {self.joints.__repr__()}'
		s += f'\n	* weird_padding_2 = {self.weird_padding_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
