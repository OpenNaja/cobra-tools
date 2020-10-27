import typing
from generated.array import Array
from generated.formats.ms2.compound.JointCompound import JointCompound
from generated.formats.ms2.compound.JweBone import JweBone
from generated.formats.ms2.compound.Matrix44 import Matrix44
from generated.formats.ms2.compound.PcJointBone import PcJointBone
from generated.formats.ms2.compound.PcJointNext import PcJointNext
from generated.formats.ms2.compound.PzBone import PzBone
from generated.formats.ms2.compound.UnkHierlistEntry import UnkHierlistEntry
from generated.formats.ms2.compound.ZStringBuffer import ZStringBuffer


class PcJoints:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# may be padding
		self.unk_zero = 0

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
		self.unknown_24 = 0
		self.unknown_28 = 0
		self.unknown_2_c = 0
		self.unknown_30 = 0
		self.unknown_34 = 0

		# index count3
		self.bone_count = 0
		self.unknown_40 = 0
		self.unknown_44 = 0

		# index count4
		self.bone_parents_count = 0

		# pZ only
		self.extra_uint_0 = 0

		# index count 5
		self.count_5 = 0
		self.unknown_58 = 0
		self.unknown_5_c = 0

		# always 1
		self.one_64 = 0

		# if joints are present, same as bone count
		self.unk_joint_count = 0

		# index count 7
		self.count_7 = 0

		# joint count
		self.joint_count = 0
		self.unknown_7_c = 0

		# unnk 78 count
		self.unk_78_count = 0
		self.unknown_84 = 0

		# jwe only, everything is shifted a bit due to extra uint 0
		self.unknown_88 = 0

		# same as above
		self.unknown_8_c = 0

		# same as above
		self.unknownextra = 0

		# uses ushort here
		self.name_indices = Array()

		# zeros. One index occupies 2 bytes; pad to multiples of 16 bytes.
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

		# unclear what this is doing
		self.unknown_hier_list = Array()

		# unique here! -1
		self.parent_indices = Array()

		# guess
		self.parent_padding = Array()

		# may be fixed
		self.zeros = Array()

		# may be fixed
		self.joint_info = JointCompound()
		self.some_floats = Array()
		self.some_next_stuff = Array()

		# may be fixed
		self.zeros_b = Array()
		self.some_count = 0

		# -1, 16 bytes
		self.some_minus_ones = Array()
		self.names = ZStringBuffer()

	def read(self, stream):

		self.io_start = stream.tell()
		self.unk_zero = stream.read_uint64()
		self.name_count = stream.read_int()
		self.float_0_1 = stream.read_float()
		self.knownff = stream.read_ushort()
		self.zero_0 = stream.read_ushort()
		self.unknown_0_c = stream.read_uint()
		self.unk_count = stream.read_uint()
		self.unknown_14 = stream.read_uint()
		self.bind_matrix_count = stream.read_uint()
		self.int_0_1 = stream.read_uint()
		self.unknown_20 = stream.read_uint()
		self.unknown_24 = stream.read_uint()
		self.unknown_28 = stream.read_uint()
		self.unknown_2_c = stream.read_uint()
		self.unknown_30 = stream.read_uint()
		self.unknown_34 = stream.read_uint()
		self.bone_count = stream.read_uint64()
		self.unknown_40 = stream.read_uint()
		self.unknown_44 = stream.read_uint()
		self.bone_parents_count = stream.read_uint64()
		if (stream.user_version == 8340) and (stream.version == 19):
			self.extra_uint_0 = stream.read_uint64()
		self.count_5 = stream.read_uint64()
		self.unknown_58 = stream.read_uint()
		self.unknown_5_c = stream.read_uint()
		self.one_64 = stream.read_uint64()
		self.unk_joint_count = stream.read_uint64()
		if not (stream.version == 18):
			self.count_7 = stream.read_uint64()
		self.joint_count = stream.read_uint()
		self.unknown_7_c = stream.read_uint()
		self.unk_78_count = stream.read_uint()
		self.unknown_84 = stream.read_uint()
		if ((stream.user_version == 24724) and (stream.version == 19)) or (stream.version == 18):
			self.unknown_88 = stream.read_uint()
			self.unknown_8_c = stream.read_uint()
		if stream.version == 18:
			self.unknownextra = stream.read_uint64()
		self.name_indices.read(stream, 'Ushort', self.name_count, None)
		self.name_padding.read(stream, 'Byte', (16 - ((self.name_count * 2) % 16)) % 16, None)
		self.inverse_bind_matrices.read(stream, Matrix44, self.bind_matrix_count, None)
		if (stream.user_version == 8340) and (stream.version == 19):
			self.bones.read(stream, PzBone, self.bone_count, None)
		if ((stream.user_version == 24724) and (stream.version == 19)) or (stream.version == 18):
			self.bones.read(stream, JweBone, self.bone_count, None)
		self.bone_parents.read(stream, 'Ubyte', self.bone_parents_count, None)
		self.hier_1_padding.read(stream, 'Byte', (8 - (self.bone_parents_count % 8)) % 8, None)
		if self.one_64:
			self.unknown_hier_list.read(stream, UnkHierlistEntry, self.count_5, None)
		self.parent_indices.read(stream, 'Short', self.bone_count, None)
		self.parent_padding.read(stream, 'Byte', (16 - ((self.name_count * 2) % 16)) % 16, None)
		self.zeros.read(stream, 'Uint64', 5, None)
		self.joint_info = stream.read_type(JointCompound)
		self.some_floats.read(stream, PcJointBone, self.joint_info.bone_count, None)
		self.some_next_stuff.read(stream, PcJointNext, self.joint_info.bone_count, None)
		self.zeros_b.read(stream, 'Uint', 5, None)
		self.some_count = stream.read_uint()
		self.some_minus_ones.read(stream, 'Int', self.some_count, None)
		self.names = stream.read_type(ZStringBuffer, (self.joint_info.namespace_length,))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64(self.unk_zero)
		stream.write_int(self.name_count)
		stream.write_float(self.float_0_1)
		stream.write_ushort(self.knownff)
		stream.write_ushort(self.zero_0)
		stream.write_uint(self.unknown_0_c)
		stream.write_uint(self.unk_count)
		stream.write_uint(self.unknown_14)
		stream.write_uint(self.bind_matrix_count)
		stream.write_uint(self.int_0_1)
		stream.write_uint(self.unknown_20)
		stream.write_uint(self.unknown_24)
		stream.write_uint(self.unknown_28)
		stream.write_uint(self.unknown_2_c)
		stream.write_uint(self.unknown_30)
		stream.write_uint(self.unknown_34)
		stream.write_uint64(self.bone_count)
		stream.write_uint(self.unknown_40)
		stream.write_uint(self.unknown_44)
		stream.write_uint64(self.bone_parents_count)
		if (stream.user_version == 8340) and (stream.version == 19):
			stream.write_uint64(self.extra_uint_0)
		stream.write_uint64(self.count_5)
		stream.write_uint(self.unknown_58)
		stream.write_uint(self.unknown_5_c)
		stream.write_uint64(self.one_64)
		stream.write_uint64(self.unk_joint_count)
		if not (stream.version == 18):
			stream.write_uint64(self.count_7)
		stream.write_uint(self.joint_count)
		stream.write_uint(self.unknown_7_c)
		stream.write_uint(self.unk_78_count)
		stream.write_uint(self.unknown_84)
		if ((stream.user_version == 24724) and (stream.version == 19)) or (stream.version == 18):
			stream.write_uint(self.unknown_88)
			stream.write_uint(self.unknown_8_c)
		if stream.version == 18:
			stream.write_uint64(self.unknownextra)
		self.name_indices.write(stream, 'Ushort', self.name_count, None)
		self.name_padding.write(stream, 'Byte', (16 - ((self.name_count * 2) % 16)) % 16, None)
		self.inverse_bind_matrices.write(stream, Matrix44, self.bind_matrix_count, None)
		if (stream.user_version == 8340) and (stream.version == 19):
			self.bones.write(stream, PzBone, self.bone_count, None)
		if ((stream.user_version == 24724) and (stream.version == 19)) or (stream.version == 18):
			self.bones.write(stream, JweBone, self.bone_count, None)
		self.bone_parents.write(stream, 'Ubyte', self.bone_parents_count, None)
		self.hier_1_padding.write(stream, 'Byte', (8 - (self.bone_parents_count % 8)) % 8, None)
		if self.one_64:
			self.unknown_hier_list.write(stream, UnkHierlistEntry, self.count_5, None)
		self.parent_indices.write(stream, 'Short', self.bone_count, None)
		self.parent_padding.write(stream, 'Byte', (16 - ((self.name_count * 2) % 16)) % 16, None)
		self.zeros.write(stream, 'Uint64', 5, None)
		stream.write_type(self.joint_info)
		self.some_floats.write(stream, PcJointBone, self.joint_info.bone_count, None)
		self.some_next_stuff.write(stream, PcJointNext, self.joint_info.bone_count, None)
		self.zeros_b.write(stream, 'Uint', 5, None)
		stream.write_uint(self.some_count)
		self.some_minus_ones.write(stream, 'Int', self.some_count, None)
		stream.write_type(self.names)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'PcJoints [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* unk_zero = ' + self.unk_zero.__repr__()
		s += '\n	* name_count = ' + self.name_count.__repr__()
		s += '\n	* float_0_1 = ' + self.float_0_1.__repr__()
		s += '\n	* knownff = ' + self.knownff.__repr__()
		s += '\n	* zero_0 = ' + self.zero_0.__repr__()
		s += '\n	* unknown_0_c = ' + self.unknown_0_c.__repr__()
		s += '\n	* unk_count = ' + self.unk_count.__repr__()
		s += '\n	* unknown_14 = ' + self.unknown_14.__repr__()
		s += '\n	* bind_matrix_count = ' + self.bind_matrix_count.__repr__()
		s += '\n	* int_0_1 = ' + self.int_0_1.__repr__()
		s += '\n	* unknown_20 = ' + self.unknown_20.__repr__()
		s += '\n	* unknown_24 = ' + self.unknown_24.__repr__()
		s += '\n	* unknown_28 = ' + self.unknown_28.__repr__()
		s += '\n	* unknown_2_c = ' + self.unknown_2_c.__repr__()
		s += '\n	* unknown_30 = ' + self.unknown_30.__repr__()
		s += '\n	* unknown_34 = ' + self.unknown_34.__repr__()
		s += '\n	* bone_count = ' + self.bone_count.__repr__()
		s += '\n	* unknown_40 = ' + self.unknown_40.__repr__()
		s += '\n	* unknown_44 = ' + self.unknown_44.__repr__()
		s += '\n	* bone_parents_count = ' + self.bone_parents_count.__repr__()
		s += '\n	* extra_uint_0 = ' + self.extra_uint_0.__repr__()
		s += '\n	* count_5 = ' + self.count_5.__repr__()
		s += '\n	* unknown_58 = ' + self.unknown_58.__repr__()
		s += '\n	* unknown_5_c = ' + self.unknown_5_c.__repr__()
		s += '\n	* one_64 = ' + self.one_64.__repr__()
		s += '\n	* unk_joint_count = ' + self.unk_joint_count.__repr__()
		s += '\n	* count_7 = ' + self.count_7.__repr__()
		s += '\n	* joint_count = ' + self.joint_count.__repr__()
		s += '\n	* unknown_7_c = ' + self.unknown_7_c.__repr__()
		s += '\n	* unk_78_count = ' + self.unk_78_count.__repr__()
		s += '\n	* unknown_84 = ' + self.unknown_84.__repr__()
		s += '\n	* unknown_88 = ' + self.unknown_88.__repr__()
		s += '\n	* unknown_8_c = ' + self.unknown_8_c.__repr__()
		s += '\n	* unknownextra = ' + self.unknownextra.__repr__()
		s += '\n	* name_indices = ' + self.name_indices.__repr__()
		s += '\n	* name_padding = ' + self.name_padding.__repr__()
		s += '\n	* inverse_bind_matrices = ' + self.inverse_bind_matrices.__repr__()
		s += '\n	* bones = ' + self.bones.__repr__()
		s += '\n	* bone_parents = ' + self.bone_parents.__repr__()
		s += '\n	* hier_1_padding = ' + self.hier_1_padding.__repr__()
		s += '\n	* unknown_hier_list = ' + self.unknown_hier_list.__repr__()
		s += '\n	* parent_indices = ' + self.parent_indices.__repr__()
		s += '\n	* parent_padding = ' + self.parent_padding.__repr__()
		s += '\n	* zeros = ' + self.zeros.__repr__()
		s += '\n	* joint_info = ' + self.joint_info.__repr__()
		s += '\n	* some_floats = ' + self.some_floats.__repr__()
		s += '\n	* some_next_stuff = ' + self.some_next_stuff.__repr__()
		s += '\n	* zeros_b = ' + self.zeros_b.__repr__()
		s += '\n	* some_count = ' + self.some_count.__repr__()
		s += '\n	* some_minus_ones = ' + self.some_minus_ones.__repr__()
		s += '\n	* names = ' + self.names.__repr__()
		s += '\n'
		return s
