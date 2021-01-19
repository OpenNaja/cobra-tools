import typing
from generated.array import Array
from generated.formats.ms2.compound.JweBone import JweBone
from generated.formats.ms2.compound.Matrix44 import Matrix44
from generated.formats.ms2.compound.PzBone import PzBone
from generated.formats.ms2.compound.Struct7 import Struct7
from generated.formats.ms2.compound.ZerosPadding import ZerosPadding


class Ms2BoneInfo:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# index count 1, setting to int to fix boneless model import
		self.name_count = 0

		# seems to be either 0.0 or 1.0
		self.float_0_1 = 0

		# this is always FFFF for now
		self.knownff = 0

		# this is always 0000 for now
		self.zero_0 = 0
		self.unknown_0_c = 0

		# almost always 4, 1 for male african lion
		self.unk_count = 0
		self.unknown_14 = 0

		# seems to match bone count
		self.bind_matrix_count = 0

		# usually 0; 1 for animal_box_large, animal_box_medium_static
		self.int_0_1 = 0
		self.unknown_20 = 0
		self.unknown_28 = 0
		self.unknown_30 = 0

		# index count3
		self.bone_count = 0
		self.unknown_40 = 0

		# index count4
		self.bone_parents_count = 0

		# pZ only
		self.extra_uint_0 = 0

		# index count 5
		self.count_5 = 0
		self.unknown_58 = 0

		# always 1
		self.one = 0

		# this counts the weird padding at the end, usually == bone count, 0 in PZ aardvark
		self.zeros_count = 0

		# index count 7
		self.count_7 = 0

		# joint count
		self.joint_count = 0

		# unnk 78 count
		self.unk_78_count = 0

		# jwe only, everything is shifted a bit due to extra uint 0
		self.unknown_88 = 0

		# same as above
		self.unknownextra = 0

		# index into ms2 string table for bones used here
		self.name_indices = Array()

		# zeros. One index occupies 4 bytes; pad to multiples of 16 bytes.
		self.name_padding = Array()

		# used for skinning
		self.inverse_bind_matrices = Array()

		# bones, rot first
		self.bones = Array()

		# bones, loc first
		self.bones = Array()

		# 255 = root, index in this list is the current bone index, value is the bone's parent index
		self.bone_parents = Array()

		# zeros
		self.hier_1_padding = Array()

		# enumerates all bone indices, 4 may be flags
		self.enumeration = Array()

		# weird zeros
		self.zeros_padding = ZerosPadding()

		# not present for static objects
		self.struct_7 = Struct7()

	def read(self, stream):

		self.io_start = stream.tell()
		self.name_count = stream.read_int()
		self.float_0_1 = stream.read_float()
		self.knownff = stream.read_ushort()
		self.zero_0 = stream.read_ushort()
		self.unknown_0_c = stream.read_uint()
		self.unk_count = stream.read_uint()
		self.unknown_14 = stream.read_uint()
		self.bind_matrix_count = stream.read_uint()
		self.int_0_1 = stream.read_uint()
		self.unknown_20 = stream.read_uint64()
		self.unknown_28 = stream.read_uint64()
		self.unknown_30 = stream.read_uint64()
		self.bone_count = stream.read_uint64()
		self.unknown_40 = stream.read_uint64()
		self.bone_parents_count = stream.read_uint64()
		if ((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version == 19):
			self.extra_uint_0 = stream.read_uint64()
		self.count_5 = stream.read_uint64()
		self.unknown_58 = stream.read_uint64()
		self.one = stream.read_uint64()
		self.zeros_count = stream.read_uint64()
		if not (stream.version == 18):
			self.count_7 = stream.read_uint64()
		self.joint_count = stream.read_uint64()
		self.unk_78_count = stream.read_uint64()
		if (((stream.user_version == 24724) or (stream.user_version == 25108)) and ((stream.version == 19) and (stream.version_flag == 1))) or (stream.version == 18):
			self.unknown_88 = stream.read_uint64()
		if stream.version == 18:
			self.unknownextra = stream.read_uint64()
		self.name_indices = stream.read_uints((self.name_count))
		self.name_padding = stream.read_bytes(((16 - ((self.name_count * 4) % 16)) % 16))
		self.inverse_bind_matrices.read(stream, Matrix44, self.bind_matrix_count, None)
		if ((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version == 19):
			self.bones.read(stream, PzBone, self.bone_count, None)
		if (((stream.user_version == 24724) or (stream.user_version == 25108)) and ((stream.version == 19) and (stream.version_flag == 1))) or (stream.version == 18):
			self.bones.read(stream, JweBone, self.bone_count, None)
		self.bone_parents = stream.read_ubytes((self.bone_parents_count))
		self.hier_1_padding = stream.read_bytes(((8 - (self.bone_parents_count % 8)) % 8))
		if self.one:
			self.enumeration = stream.read_uints((self.count_5, 2))
		if self.zeros_count:
			self.zeros_padding = stream.read_type(ZerosPadding, (self.zeros_count,))
		if self.count_7:
			self.struct_7 = stream.read_type(Struct7)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_int(self.name_count)
		stream.write_float(self.float_0_1)
		stream.write_ushort(self.knownff)
		stream.write_ushort(self.zero_0)
		stream.write_uint(self.unknown_0_c)
		stream.write_uint(self.unk_count)
		stream.write_uint(self.unknown_14)
		stream.write_uint(self.bind_matrix_count)
		stream.write_uint(self.int_0_1)
		stream.write_uint64(self.unknown_20)
		stream.write_uint64(self.unknown_28)
		stream.write_uint64(self.unknown_30)
		stream.write_uint64(self.bone_count)
		stream.write_uint64(self.unknown_40)
		stream.write_uint64(self.bone_parents_count)
		if ((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version == 19):
			stream.write_uint64(self.extra_uint_0)
		stream.write_uint64(self.count_5)
		stream.write_uint64(self.unknown_58)
		stream.write_uint64(self.one)
		stream.write_uint64(self.zeros_count)
		if not (stream.version == 18):
			stream.write_uint64(self.count_7)
		stream.write_uint64(self.joint_count)
		stream.write_uint64(self.unk_78_count)
		if (((stream.user_version == 24724) or (stream.user_version == 25108)) and ((stream.version == 19) and (stream.version_flag == 1))) or (stream.version == 18):
			stream.write_uint64(self.unknown_88)
		if stream.version == 18:
			stream.write_uint64(self.unknownextra)
		stream.write_uints(self.name_indices)
		stream.write_bytes(self.name_padding)
		self.inverse_bind_matrices.write(stream, Matrix44, self.bind_matrix_count, None)
		if ((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version == 19):
			self.bones.write(stream, PzBone, self.bone_count, None)
		if (((stream.user_version == 24724) or (stream.user_version == 25108)) and ((stream.version == 19) and (stream.version_flag == 1))) or (stream.version == 18):
			self.bones.write(stream, JweBone, self.bone_count, None)
		stream.write_ubytes(self.bone_parents)
		stream.write_bytes(self.hier_1_padding)
		if self.one:
			stream.write_uints(self.enumeration)
		if self.zeros_count:
			stream.write_type(self.zeros_padding)
		if self.count_7:
			stream.write_type(self.struct_7)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Ms2BoneInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* name_count = {self.name_count.__repr__()}'
		s += f'\n	* float_0_1 = {self.float_0_1.__repr__()}'
		s += f'\n	* knownff = {self.knownff.__repr__()}'
		s += f'\n	* zero_0 = {self.zero_0.__repr__()}'
		s += f'\n	* unknown_0_c = {self.unknown_0_c.__repr__()}'
		s += f'\n	* unk_count = {self.unk_count.__repr__()}'
		s += f'\n	* unknown_14 = {self.unknown_14.__repr__()}'
		s += f'\n	* bind_matrix_count = {self.bind_matrix_count.__repr__()}'
		s += f'\n	* int_0_1 = {self.int_0_1.__repr__()}'
		s += f'\n	* unknown_20 = {self.unknown_20.__repr__()}'
		s += f'\n	* unknown_28 = {self.unknown_28.__repr__()}'
		s += f'\n	* unknown_30 = {self.unknown_30.__repr__()}'
		s += f'\n	* bone_count = {self.bone_count.__repr__()}'
		s += f'\n	* unknown_40 = {self.unknown_40.__repr__()}'
		s += f'\n	* bone_parents_count = {self.bone_parents_count.__repr__()}'
		s += f'\n	* extra_uint_0 = {self.extra_uint_0.__repr__()}'
		s += f'\n	* count_5 = {self.count_5.__repr__()}'
		s += f'\n	* unknown_58 = {self.unknown_58.__repr__()}'
		s += f'\n	* one = {self.one.__repr__()}'
		s += f'\n	* zeros_count = {self.zeros_count.__repr__()}'
		s += f'\n	* count_7 = {self.count_7.__repr__()}'
		s += f'\n	* joint_count = {self.joint_count.__repr__()}'
		s += f'\n	* unk_78_count = {self.unk_78_count.__repr__()}'
		s += f'\n	* unknown_88 = {self.unknown_88.__repr__()}'
		s += f'\n	* unknownextra = {self.unknownextra.__repr__()}'
		s += f'\n	* name_indices = {self.name_indices.__repr__()}'
		s += f'\n	* name_padding = {self.name_padding.__repr__()}'
		s += f'\n	* inverse_bind_matrices = {self.inverse_bind_matrices.__repr__()}'
		s += f'\n	* bones = {self.bones.__repr__()}'
		s += f'\n	* bone_parents = {self.bone_parents.__repr__()}'
		s += f'\n	* hier_1_padding = {self.hier_1_padding.__repr__()}'
		s += f'\n	* enumeration = {self.enumeration.__repr__()}'
		s += f'\n	* zeros_padding = {self.zeros_padding.__repr__()}'
		s += f'\n	* struct_7 = {self.struct_7.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
