import numpy
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

	def __init__(self, context, arg=0, template=None, set_default=True):
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
		self.zeros = numpy.zeros((3,), dtype=numpy.dtype('uint64'))
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
		self.name_indices = numpy.zeros((self.name_count,), dtype=numpy.dtype('uint32'))

		# index into ms2 string table for bones used here
		self.name_indices = numpy.zeros((self.name_count,), dtype=numpy.dtype('uint16'))

		# zeros. One index occupies 4 bytes; pad to multiples of 16 bytes.
		self.name_padding = numpy.zeros(((16 - ((self.name_count * 4) % 16)) % 16,), dtype=numpy.dtype('int8'))

		# zeros. One index occupies 4 bytes; pad to multiples of 16 bytes.
		self.name_padding = numpy.zeros(((16 - ((self.name_count * 2) % 16)) % 16,), dtype=numpy.dtype('int8'))

		# used for skinning
		self.inverse_bind_matrices = Array((self.bind_matrix_count,), Matrix44, self.context, 0, None)
		self.bones = Array((self.bone_count,), Bone, self.context, 0, None)

		# 255 = root, index in this list is the current bone index, value is the bone's parent index
		self.parents = numpy.zeros((self.parents_count,), dtype=numpy.dtype('uint8'))

		# zeros
		self.parents_padding = numpy.zeros(((8 - (self.parents_count % 8)) % 8,), dtype=numpy.dtype('int8'))

		# enumerates all bone indices, 4 may be flags
		self.enumeration = numpy.zeros((self.enum_count, 2,), dtype=numpy.dtype('uint32'))

		# enumerates all bone indices, 4 may be flags
		self.enumeration = numpy.zeros((self.enum_count,), dtype=numpy.dtype('uint8'))

		# zeros
		self.zt_weirdness = numpy.zeros((10,), dtype=numpy.dtype('int16'))

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
		self.name_count = 0
		if self.context.version >= 32:
			self.knownff = 0
		if self.context.version >= 32:
			self.zero_0 = 0
		if self.context.version >= 32:
			self.unknown_0_c = 0
		self.unk_count = 0
		self.bind_matrix_count = 0
		self.zeros = numpy.zeros((3,), dtype=numpy.dtype('uint64'))
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
			self.name_indices = numpy.zeros((self.name_count,), dtype=numpy.dtype('uint32'))
		if self.context.version < 47:
			self.name_indices = numpy.zeros((self.name_count,), dtype=numpy.dtype('uint16'))
		if not (self.context.version < 47):
			self.name_padding = numpy.zeros(((16 - ((self.name_count * 4) % 16)) % 16,), dtype=numpy.dtype('int8'))
		if self.context.version < 47:
			self.name_padding = numpy.zeros(((16 - ((self.name_count * 2) % 16)) % 16,), dtype=numpy.dtype('int8'))
		self.inverse_bind_matrices = Array((self.bind_matrix_count,), Matrix44, self.context, 0, None)
		self.bones = Array((self.bone_count,), Bone, self.context, 0, None)
		self.parents = numpy.zeros((self.parents_count,), dtype=numpy.dtype('uint8'))
		if not (self.context.version == 13):
			self.parents_padding = numpy.zeros(((8 - (self.parents_count % 8)) % 8,), dtype=numpy.dtype('int8'))
		if not (self.context.version == 13) and self.one:
			self.enumeration = numpy.zeros((self.enum_count, 2,), dtype=numpy.dtype('uint32'))
		if self.context.version == 13 and self.one:
			self.enumeration = numpy.zeros((self.enum_count,), dtype=numpy.dtype('uint8'))
		if self.context.version == 13:
			self.zt_weirdness = numpy.zeros((10,), dtype=numpy.dtype('int16'))
		if not (self.context.version < 47) and self.zeros_count:
			self.zeros_padding = ZerosPadding(self.context, self.zeros_count, None)
		if self.context.version < 47 and self.zeros_count:
			self.minus_padding = MinusPadding(self.context, self.zeros_count, None)
		if self.count_7:
			self.struct_7 = Struct7(self.context, 0, None)
		if self.joint_count:
			self.joints = JointData(self.context, 0, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		instance.name_count = stream.read_uint64()
		if instance.context.version >= 32:
			instance.knownff = stream.read_short()
			instance.zero_0 = stream.read_short()
		if instance.context.version >= 32:
			instance.unknown_0_c = stream.read_uint()
		instance.unk_count = stream.read_uint64()
		instance.bind_matrix_count = stream.read_uint64()
		instance.zeros = stream.read_uint64s((3,))
		instance.bone_count = stream.read_uint64()
		instance.unknown_40 = stream.read_uint64()
		instance.parents_count = stream.read_uint64()
		if (instance.context.version == 13) or (((instance.context.version == 48) or (instance.context.version == 50)) or (instance.context.version == 51)):
			instance.extra_zero = stream.read_uint64()
		instance.enum_count = stream.read_uint64()
		instance.unknown_58 = stream.read_uint64()
		instance.one = stream.read_uint64()
		instance.zeros_count = stream.read_uint64()
		if instance.context.version == 32:
			instance.unk_pc_count = stream.read_uint64()
		instance.count_7 = stream.read_uint64()
		instance.joint_count = stream.read_uint64()
		instance.unk_78_count = stream.read_uint64()
		if instance.context.version <= 13:
			instance.unk_extra = stream.read_uint64()
		if (instance.context.version == 47) or (instance.context.version == 39):
			instance.unk_extra_jwe = stream.read_uint64()
		if not (instance.context.version < 47):
			instance.name_indices = stream.read_uints((instance.name_count,))
		if instance.context.version < 47:
			instance.name_indices = stream.read_ushorts((instance.name_count,))
		if not (instance.context.version < 47):
			instance.name_padding = stream.read_bytes(((16 - ((instance.name_count * 4) % 16)) % 16,))
		if instance.context.version < 47:
			instance.name_padding = stream.read_bytes(((16 - ((instance.name_count * 2) % 16)) % 16,))
		instance.inverse_bind_matrices = Array.from_stream(stream, (instance.bind_matrix_count,), Matrix44, instance.context, 0, None)
		instance.bones = Array.from_stream(stream, (instance.bone_count,), Bone, instance.context, 0, None)
		instance.parents = stream.read_ubytes((instance.parents_count,))
		if not (instance.context.version == 13):
			instance.parents_padding = stream.read_bytes(((8 - (instance.parents_count % 8)) % 8,))
		if not (instance.context.version == 13) and instance.one:
			instance.enumeration = stream.read_uints((instance.enum_count, 2,))
		if instance.context.version == 13 and instance.one:
			instance.enumeration = stream.read_ubytes((instance.enum_count,))
		if instance.context.version == 13:
			instance.zt_weirdness = stream.read_shorts((10,))
		if not (instance.context.version < 47) and instance.zeros_count:
			instance.zeros_padding = ZerosPadding.from_stream(stream, instance.context, instance.zeros_count, None)
		if instance.context.version < 47 and instance.zeros_count:
			instance.minus_padding = MinusPadding.from_stream(stream, instance.context, instance.zeros_count, None)
		if instance.count_7:
			instance.struct_7 = Struct7.from_stream(stream, instance.context, 0, None)
		if instance.joint_count:
			instance.joints = JointData.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint64(instance.name_count)
		if instance.context.version >= 32:
			stream.write_short(instance.knownff)
			stream.write_short(instance.zero_0)
		if instance.context.version >= 32:
			stream.write_uint(instance.unknown_0_c)
		stream.write_uint64(instance.unk_count)
		stream.write_uint64(instance.bind_matrix_count)
		stream.write_uint64s(instance.zeros)
		stream.write_uint64(instance.bone_count)
		stream.write_uint64(instance.unknown_40)
		stream.write_uint64(instance.parents_count)
		if (instance.context.version == 13) or (((instance.context.version == 48) or (instance.context.version == 50)) or (instance.context.version == 51)):
			stream.write_uint64(instance.extra_zero)
		stream.write_uint64(instance.enum_count)
		stream.write_uint64(instance.unknown_58)
		stream.write_uint64(instance.one)
		stream.write_uint64(instance.zeros_count)
		if instance.context.version == 32:
			stream.write_uint64(instance.unk_pc_count)
		stream.write_uint64(instance.count_7)
		stream.write_uint64(instance.joint_count)
		stream.write_uint64(instance.unk_78_count)
		if instance.context.version <= 13:
			stream.write_uint64(instance.unk_extra)
		if (instance.context.version == 47) or (instance.context.version == 39):
			stream.write_uint64(instance.unk_extra_jwe)
		if not (instance.context.version < 47):
			stream.write_uints(instance.name_indices)
		if instance.context.version < 47:
			stream.write_ushorts(instance.name_indices)
		if not (instance.context.version < 47):
			instance.name_padding.resize(((16 - ((instance.name_count * 4) % 16)) % 16,))
			stream.write_bytes(instance.name_padding)
		if instance.context.version < 47:
			instance.name_padding.resize(((16 - ((instance.name_count * 2) % 16)) % 16,))
			stream.write_bytes(instance.name_padding)
		Array.to_stream(stream, instance.inverse_bind_matrices, (instance.bind_matrix_count,), Matrix44, instance.context, 0, None)
		Array.to_stream(stream, instance.bones, (instance.bone_count,), Bone, instance.context, 0, None)
		stream.write_ubytes(instance.parents)
		if not (instance.context.version == 13):
			instance.parents_padding.resize(((8 - (instance.parents_count % 8)) % 8,))
			stream.write_bytes(instance.parents_padding)
		if not (instance.context.version == 13) and instance.one:
			stream.write_uints(instance.enumeration)
		if instance.context.version == 13 and instance.one:
			stream.write_ubytes(instance.enumeration)
		if instance.context.version == 13:
			stream.write_shorts(instance.zt_weirdness)
		if not (instance.context.version < 47) and instance.zeros_count:
			ZerosPadding.to_stream(stream, instance.zeros_padding)
		if instance.context.version < 47 and instance.zeros_count:
			MinusPadding.to_stream(stream, instance.minus_padding)
		if instance.count_7:
			Struct7.to_stream(stream, instance.struct_7)
		if instance.joint_count:
			JointData.to_stream(stream, instance.joints)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

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
