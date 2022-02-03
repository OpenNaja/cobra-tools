import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.Bone import Bone
from generated.formats.ms2.compound.JointData import JointData
from generated.formats.ms2.compound.Matrix44 import Matrix44
from generated.formats.ms2.compound.MinusPadding import MinusPadding
from generated.formats.ms2.compound.Struct7 import Struct7
from generated.formats.ms2.compound.ZerosPadding import ZerosPadding


class BoneInfo:

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
		self.knownff = 0

		# this is always 0000 for now
		self.zero_0 = 0
		self.unknown_0_c = 0

		# almost always 4, 1 for male african lion
		self.unk_count = 0

		# seems to match bone count
		self.bind_matrix_count = 0
		self.zeros = numpy.zeros((3), dtype='uint64')
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

		# index into ms2 string table for bones used here
		self.name_indices = numpy.zeros((self.name_count), dtype='uint')

		# index into ms2 string table for bones used here
		self.name_indices = numpy.zeros((self.name_count), dtype='ushort')

		# zeros. One index occupies 4 bytes; pad to multiples of 16 bytes.
		self.name_padding = numpy.zeros(((16 - ((self.name_count * 4) % 16)) % 16), dtype='byte')

		# zeros. One index occupies 4 bytes; pad to multiples of 16 bytes.
		self.name_padding = numpy.zeros(((16 - ((self.name_count * 2) % 16)) % 16), dtype='byte')

		# used for skinning
		self.inverse_bind_matrices = Array(self.context)
		self.bones = Array(self.context)

		# 255 = root, index in this list is the current bone index, value is the bone's parent index
		self.parents = numpy.zeros((self.parents_count), dtype='ubyte')

		# zeros
		self.parents_padding = numpy.zeros(((8 - (self.parents_count % 8)) % 8), dtype='byte')

		# enumerates all bone indices, 4 may be flags
		self.enumeration = numpy.zeros((self.enum_count, 2), dtype='uint')

		# enumerates all bone indices, 4 may be flags
		self.enumeration = numpy.zeros((self.enum_count), dtype='ubyte')

		# zeros
		self.zt_weirdness = numpy.zeros((10), dtype='short')

		# weird zeros
		self.zeros_padding = ZerosPadding(self.context, self.zeros_count, None)

		# weird -1s
		self.minus_padding = MinusPadding(self.context, self.zeros_count, None)

		# ragdoll links?
		self.struct_7 = Struct7(self.context, None, None)

		# joints
		self.joints = JointData(self.context, None, None)
		self.set_defaults()

	def set_defaults(self):
		self.name_count = 0
		if self.context.version >= 32:
			self.knownff = 0
		if self.context.version >= 32:
			self.zero_0 = 0
		if self.context.version >= 32:
			self.unknown_0_c = 0
		self.unk_count = 0
		self.bind_matrix_count = 0
		self.zeros = numpy.zeros((3), dtype='uint64')
		self.bone_count = 0
		self.unknown_40 = 0
		self.parents_count = 0
		if (self.context.version == 13) or (((self.context.version == 48) or (self.context.version == 50)) or (self.context.version == 51)):
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
			self.name_indices = numpy.zeros((self.name_count), dtype='uint')
		if self.context.version < 47:
			self.name_indices = numpy.zeros((self.name_count), dtype='ushort')
		if not (self.context.version < 47):
			self.name_padding = numpy.zeros(((16 - ((self.name_count * 4) % 16)) % 16), dtype='byte')
		if self.context.version < 47:
			self.name_padding = numpy.zeros(((16 - ((self.name_count * 2) % 16)) % 16), dtype='byte')
		self.inverse_bind_matrices = Array(self.context)
		self.bones = Array(self.context)
		self.parents = numpy.zeros((self.parents_count), dtype='ubyte')
		if not (self.context.version == 13):
			self.parents_padding = numpy.zeros(((8 - (self.parents_count % 8)) % 8), dtype='byte')
		if not (self.context.version == 13) and self.one:
			self.enumeration = numpy.zeros((self.enum_count, 2), dtype='uint')
		if self.context.version == 13 and self.one:
			self.enumeration = numpy.zeros((self.enum_count), dtype='ubyte')
		if self.context.version == 13:
			self.zt_weirdness = numpy.zeros((10), dtype='short')
		if not (self.context.version < 47) and self.zeros_count:
			self.zeros_padding = ZerosPadding(self.context, self.zeros_count, None)
		if self.context.version < 47 and self.zeros_count:
			self.minus_padding = MinusPadding(self.context, self.zeros_count, None)
		if self.count_7:
			self.struct_7 = Struct7(self.context, None, None)
		if self.joint_count:
			self.joints = JointData(self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.name_count = stream.read_uint64()
		if self.context.version >= 32:
			self.knownff = stream.read_short()
			self.zero_0 = stream.read_short()
		if self.context.version >= 32:
			self.unknown_0_c = stream.read_uint()
		self.unk_count = stream.read_uint64()
		self.bind_matrix_count = stream.read_uint64()
		self.zeros = stream.read_uint64s((3))
		self.bone_count = stream.read_uint64()
		self.unknown_40 = stream.read_uint64()
		self.parents_count = stream.read_uint64()
		if (self.context.version == 13) or (((self.context.version == 48) or (self.context.version == 50)) or (self.context.version == 51)):
			self.extra_zero = stream.read_uint64()
		self.enum_count = stream.read_uint64()
		self.unknown_58 = stream.read_uint64()
		self.one = stream.read_uint64()
		self.zeros_count = stream.read_uint64()
		if self.context.version == 32:
			self.unk_pc_count = stream.read_uint64()
		self.count_7 = stream.read_uint64()
		self.joint_count = stream.read_uint64()
		self.unk_78_count = stream.read_uint64()
		if self.context.version <= 13:
			self.unk_extra = stream.read_uint64()
		if (self.context.version == 47) or (self.context.version == 39):
			self.unk_extra_jwe = stream.read_uint64()
		if not (self.context.version < 47):
			self.name_indices = stream.read_uints((self.name_count))
		if self.context.version < 47:
			self.name_indices = stream.read_ushorts((self.name_count))
		if not (self.context.version < 47):
			self.name_padding = stream.read_bytes(((16 - ((self.name_count * 4) % 16)) % 16))
		if self.context.version < 47:
			self.name_padding = stream.read_bytes(((16 - ((self.name_count * 2) % 16)) % 16))
		self.inverse_bind_matrices.read(stream, Matrix44, self.bind_matrix_count, None)
		self.bones.read(stream, Bone, self.bone_count, None)
		self.parents = stream.read_ubytes((self.parents_count))
		if not (self.context.version == 13):
			self.parents_padding = stream.read_bytes(((8 - (self.parents_count % 8)) % 8))
		if not (self.context.version == 13) and self.one:
			self.enumeration = stream.read_uints((self.enum_count, 2))
		if self.context.version == 13 and self.one:
			self.enumeration = stream.read_ubytes((self.enum_count))
		if self.context.version == 13:
			self.zt_weirdness = stream.read_shorts((10))
		if not (self.context.version < 47) and self.zeros_count:
			self.zeros_padding = stream.read_type(ZerosPadding, (self.context, self.zeros_count, None))
		if self.context.version < 47 and self.zeros_count:
			self.minus_padding = stream.read_type(MinusPadding, (self.context, self.zeros_count, None))
		if self.count_7:
			self.struct_7 = stream.read_type(Struct7, (self.context, None, None))
		if self.joint_count:
			self.joints = stream.read_type(JointData, (self.context, None, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64(self.name_count)
		if self.context.version >= 32:
			stream.write_short(self.knownff)
			stream.write_short(self.zero_0)
		if self.context.version >= 32:
			stream.write_uint(self.unknown_0_c)
		stream.write_uint64(self.unk_count)
		stream.write_uint64(self.bind_matrix_count)
		stream.write_uint64s(self.zeros)
		stream.write_uint64(self.bone_count)
		stream.write_uint64(self.unknown_40)
		stream.write_uint64(self.parents_count)
		if (self.context.version == 13) or (((self.context.version == 48) or (self.context.version == 50)) or (self.context.version == 51)):
			stream.write_uint64(self.extra_zero)
		stream.write_uint64(self.enum_count)
		stream.write_uint64(self.unknown_58)
		stream.write_uint64(self.one)
		stream.write_uint64(self.zeros_count)
		if self.context.version == 32:
			stream.write_uint64(self.unk_pc_count)
		stream.write_uint64(self.count_7)
		stream.write_uint64(self.joint_count)
		stream.write_uint64(self.unk_78_count)
		if self.context.version <= 13:
			stream.write_uint64(self.unk_extra)
		if (self.context.version == 47) or (self.context.version == 39):
			stream.write_uint64(self.unk_extra_jwe)
		if not (self.context.version < 47):
			stream.write_uints(self.name_indices)
		if self.context.version < 47:
			stream.write_ushorts(self.name_indices)
		if not (self.context.version < 47):
			self.name_padding.resize(((16 - ((self.name_count * 4) % 16)) % 16))
			stream.write_bytes(self.name_padding)
		if self.context.version < 47:
			self.name_padding.resize(((16 - ((self.name_count * 2) % 16)) % 16))
			stream.write_bytes(self.name_padding)
		self.inverse_bind_matrices.write(stream, Matrix44, self.bind_matrix_count, None)
		self.bones.write(stream, Bone, self.bone_count, None)
		stream.write_ubytes(self.parents)
		if not (self.context.version == 13):
			self.parents_padding.resize(((8 - (self.parents_count % 8)) % 8))
			stream.write_bytes(self.parents_padding)
		if not (self.context.version == 13) and self.one:
			stream.write_uints(self.enumeration)
		if self.context.version == 13 and self.one:
			stream.write_ubytes(self.enumeration)
		if self.context.version == 13:
			stream.write_shorts(self.zt_weirdness)
		if not (self.context.version < 47) and self.zeros_count:
			stream.write_type(self.zeros_padding)
		if self.context.version < 47 and self.zeros_count:
			stream.write_type(self.minus_padding)
		if self.count_7:
			stream.write_type(self.struct_7)
		if self.joint_count:
			stream.write_type(self.joints)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'BoneInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

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
		s += f'\n	* parents_count = {self.parents_count.__repr__()}'
		s += f'\n	* extra_zero = {self.extra_zero.__repr__()}'
		s += f'\n	* enum_count = {self.enum_count.__repr__()}'
		s += f'\n	* unknown_58 = {self.unknown_58.__repr__()}'
		s += f'\n	* one = {self.one.__repr__()}'
		s += f'\n	* zeros_count = {self.zeros_count.__repr__()}'
		s += f'\n	* unk_pc_count = {self.unk_pc_count.__repr__()}'
		s += f'\n	* count_7 = {self.count_7.__repr__()}'
		s += f'\n	* joint_count = {self.joint_count.__repr__()}'
		s += f'\n	* unk_78_count = {self.unk_78_count.__repr__()}'
		s += f'\n	* unk_extra = {self.unk_extra.__repr__()}'
		s += f'\n	* unk_extra_jwe = {self.unk_extra_jwe.__repr__()}'
		s += f'\n	* name_indices = {self.name_indices.__repr__()}'
		s += f'\n	* name_padding = {self.name_padding.__repr__()}'
		s += f'\n	* inverse_bind_matrices = {self.inverse_bind_matrices.__repr__()}'
		s += f'\n	* bones = {self.bones.__repr__()}'
		s += f'\n	* parents = {self.parents.__repr__()}'
		s += f'\n	* parents_padding = {self.parents_padding.__repr__()}'
		s += f'\n	* enumeration = {self.enumeration.__repr__()}'
		s += f'\n	* zt_weirdness = {self.zt_weirdness.__repr__()}'
		s += f'\n	* zeros_padding = {self.zeros_padding.__repr__()}'
		s += f'\n	* minus_padding = {self.minus_padding.__repr__()}'
		s += f'\n	* struct_7 = {self.struct_7.__repr__()}'
		s += f'\n	* joints = {self.joints.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
