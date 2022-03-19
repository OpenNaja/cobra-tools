from source.formats.base.basic import fmt_member
import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.base.compound.ZStringBuffer import ZStringBuffer
from generated.formats.ms2.compound.HitcheckReader import HitcheckReader
from generated.formats.ms2.compound.JointEntry import JointEntry
from generated.formats.ms2.compound.JointInfo import JointInfo
from generated.formats.ms2.compound.ListCEntry import ListCEntry
from generated.formats.ms2.compound.ListFirst import ListFirst
from generated.formats.ms2.compound.ListLong import ListLong
from generated.formats.ms2.compound.ListShort import ListShort
from generated.formats.ms2.compound.UACJointFF import UACJointFF
from generated.formats.ovl_base.compound.SmartPadding import SmartPadding


class JointData:

	"""
	appears in dinos and static meshes
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# seemingly additional alignment, unsure about the rule
		self.start_pc = SmartPadding(self.context, 0, None)

		# repeat
		self.joint_count = 0
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0

		# 0s, might be related to count 7 in PC
		self.zeros_extra = numpy.zeros((2,), dtype=numpy.dtype('uint32'))

		# size of the name buffer below, including trailing zeros
		self.namespace_length = 0

		# 0s
		self.zeros_0 = numpy.zeros((5,), dtype=numpy.dtype('uint32'))

		# 0 or 1
		self.pc_count = 0

		# 0s
		self.zeros_1 = numpy.zeros((7,), dtype=numpy.dtype('uint32'))

		# 0s
		self.extra_zeros_pc = numpy.zeros((4,), dtype=numpy.dtype('uint32'))

		# 1, 1
		self.ones = numpy.zeros((2,), dtype=numpy.dtype('uint64'))

		# matches bone count from bone info
		self.bone_count = 0

		# 0
		self.joint_entry_count = 0

		# usually 0s
		self.zeros_2 = numpy.zeros((4,), dtype=numpy.dtype('uint32'))

		# corresponds to bone transforms
		self.joint_transforms = Array((self.joint_count,), JointEntry, self.context, 0, None)

		# might be pointers
		self.zeros_3 = numpy.zeros((self.joint_count,), dtype=numpy.dtype('uint64'))

		# ?
		self.unknown_listc = Array((self.joint_count,), ListCEntry, self.context, 0, None)

		# used by ptero, 16 bytes per entry
		self.first_list = Array((self.count_0,), ListFirst, self.context, 0, None)

		# ?
		self.short_list = Array((self.count_1,), ListShort, self.context, 0, None)

		# ?
		self.long_list = Array((self.count_2,), ListLong, self.context, 0, None)

		# old style - joint infos, without hitchecks, they are added later
		self.joint_infos = Array((self.joint_count,), UACJointFF, self.context, 0, None)

		# sometimes an array of floats
		self.pc_floats = numpy.zeros((self.pc_count, 10,), dtype=numpy.dtype('float32'))

		# index into bone info bones for each joint; bone that the joint is attached to
		self.joint_indices = numpy.zeros((self.joint_count,), dtype=numpy.dtype('int32'))

		# the inverse of the above; for each bone info bone, index of the corresponding joint or -1 if no joint
		self.bone_indices = numpy.zeros((self.bone_count,), dtype=numpy.dtype('int32'))

		# zstring name buffer
		self.joint_names = ZStringBuffer(self.context, self.namespace_length, None)

		# ?
		self.joint_names_padding = SmartPadding(self.context, 0, None)

		# new style - includes name offset, some flags and the hitchecks
		self.joint_infos = Array((self.joint_count,), JointInfo, self.context, 0, None)

		# old style - for each joint, read the hitchecks
		self.hitcheck_reader = HitcheckReader(self.context, self.joint_infos, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if self.context.version == 32:
			self.start_pc = SmartPadding(self.context, 0, None)
		self.joint_count = 0
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		if self.context.version <= 32:
			self.zeros_extra = numpy.zeros((2,), dtype=numpy.dtype('uint32'))
		self.namespace_length = 0
		self.zeros_0 = numpy.zeros((5,), dtype=numpy.dtype('uint32'))
		self.pc_count = 0
		self.zeros_1 = numpy.zeros((7,), dtype=numpy.dtype('uint32'))
		if self.context.version <= 32:
			self.extra_zeros_pc = numpy.zeros((4,), dtype=numpy.dtype('uint32'))
		self.ones = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		self.bone_count = 0
		self.joint_entry_count = 0
		self.zeros_2 = numpy.zeros((4,), dtype=numpy.dtype('uint32'))
		self.joint_transforms = Array((self.joint_count,), JointEntry, self.context, 0, None)
		if self.context.version >= 47:
			self.zeros_3 = numpy.zeros((self.joint_count,), dtype=numpy.dtype('uint64'))
		if self.context.version >= 47:
			self.unknown_listc = Array((self.joint_count,), ListCEntry, self.context, 0, None)
		if self.context.version >= 47:
			self.first_list = Array((self.count_0,), ListFirst, self.context, 0, None)
		if self.context.version >= 47:
			self.short_list = Array((self.count_1,), ListShort, self.context, 0, None)
		if self.context.version >= 47:
			self.long_list = Array((self.count_2,), ListLong, self.context, 0, None)
		if self.context.version <= 32:
			self.joint_infos = Array((self.joint_count,), UACJointFF, self.context, 0, None)
		if self.context.version <= 32:
			self.pc_floats = numpy.zeros((self.pc_count, 10,), dtype=numpy.dtype('float32'))
		self.joint_indices = numpy.zeros((self.joint_count,), dtype=numpy.dtype('int32'))
		self.bone_indices = numpy.zeros((self.bone_count,), dtype=numpy.dtype('int32'))
		self.joint_names = ZStringBuffer(self.context, self.namespace_length, None)
		self.joint_names_padding = SmartPadding(self.context, 0, None)
		if self.context.version >= 47:
			self.joint_infos = Array((self.joint_count,), JointInfo, self.context, 0, None)
		if self.context.version <= 32:
			self.hitcheck_reader = HitcheckReader(self.context, self.joint_infos, None)

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
		if instance.context.version == 32:
			instance.start_pc = SmartPadding.from_stream(stream, instance.context, 0, None)
		instance.joint_count = stream.read_uint()
		instance.count_0 = stream.read_uint()
		instance.count_1 = stream.read_uint()
		instance.count_2 = stream.read_uint()
		if instance.context.version <= 32:
			instance.zeros_extra = stream.read_uints((2,))
		instance.namespace_length = stream.read_uint()
		instance.zeros_0 = stream.read_uints((5,))
		instance.pc_count = stream.read_uint()
		instance.zeros_1 = stream.read_uints((7,))
		if instance.context.version <= 32:
			instance.extra_zeros_pc = stream.read_uints((4,))
		instance.ones = stream.read_uint64s((2,))
		instance.bone_count = stream.read_uint()
		instance.joint_entry_count = stream.read_uint()
		instance.zeros_2 = stream.read_uints((4,))
		instance.joint_transforms = Array.from_stream(stream, (instance.joint_count,), JointEntry, instance.context, 0, None)
		if instance.context.version >= 47:
			instance.zeros_3 = stream.read_uint64s((instance.joint_count,))
			instance.unknown_listc = Array.from_stream(stream, (instance.joint_count,), ListCEntry, instance.context, 0, None)
		if instance.context.version >= 47:
			instance.first_list = Array.from_stream(stream, (instance.count_0,), ListFirst, instance.context, 0, None)
			instance.short_list = Array.from_stream(stream, (instance.count_1,), ListShort, instance.context, 0, None)
		if instance.context.version >= 47:
			instance.long_list = Array.from_stream(stream, (instance.count_2,), ListLong, instance.context, 0, None)
		if instance.context.version <= 32:
			instance.joint_infos = Array.from_stream(stream, (instance.joint_count,), UACJointFF, instance.context, 0, None)
			instance.pc_floats = stream.read_floats((instance.pc_count, 10,))
		instance.joint_indices = stream.read_ints((instance.joint_count,))
		instance.bone_indices = stream.read_ints((instance.bone_count,))
		instance.joint_names = ZStringBuffer.from_stream(stream, instance.context, instance.namespace_length, None)
		instance.joint_names_padding = SmartPadding.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 47:
			instance.joint_infos = Array.from_stream(stream, (instance.joint_count,), JointInfo, instance.context, 0, None)
		if instance.context.version <= 32:
			instance.hitcheck_reader = HitcheckReader.from_stream(stream, instance.context, instance.joint_infos, None)

	@classmethod
	def write_fields(cls, stream, instance):
		if instance.context.version == 32:
			SmartPadding.to_stream(stream, instance.start_pc)
		stream.write_uint(instance.joint_count)
		stream.write_uint(instance.count_0)
		stream.write_uint(instance.count_1)
		stream.write_uint(instance.count_2)
		if instance.context.version <= 32:
			stream.write_uints(instance.zeros_extra)
		stream.write_uint(instance.namespace_length)
		stream.write_uints(instance.zeros_0)
		stream.write_uint(instance.pc_count)
		stream.write_uints(instance.zeros_1)
		if instance.context.version <= 32:
			stream.write_uints(instance.extra_zeros_pc)
		stream.write_uint64s(instance.ones)
		stream.write_uint(instance.bone_count)
		stream.write_uint(instance.joint_entry_count)
		stream.write_uints(instance.zeros_2)
		Array.to_stream(stream, instance.joint_transforms, (instance.joint_count,), JointEntry, instance.context, 0, None)
		if instance.context.version >= 47:
			stream.write_uint64s(instance.zeros_3)
			Array.to_stream(stream, instance.unknown_listc, (instance.joint_count,), ListCEntry, instance.context, 0, None)
		if instance.context.version >= 47:
			Array.to_stream(stream, instance.first_list, (instance.count_0,), ListFirst, instance.context, 0, None)
			Array.to_stream(stream, instance.short_list, (instance.count_1,), ListShort, instance.context, 0, None)
		if instance.context.version >= 47:
			Array.to_stream(stream, instance.long_list, (instance.count_2,), ListLong, instance.context, 0, None)
		if instance.context.version <= 32:
			Array.to_stream(stream, instance.joint_infos, (instance.joint_count,), UACJointFF, instance.context, 0, None)
			stream.write_floats(instance.pc_floats)
		stream.write_ints(instance.joint_indices)
		stream.write_ints(instance.bone_indices)
		ZStringBuffer.to_stream(stream, instance.joint_names)
		SmartPadding.to_stream(stream, instance.joint_names_padding)
		if instance.context.version >= 47:
			Array.to_stream(stream, instance.joint_infos, (instance.joint_count,), JointInfo, instance.context, 0, None)
		if instance.context.version <= 32:
			HitcheckReader.to_stream(stream, instance.hitcheck_reader)

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

	def get_info_str(self, indent=0):
		return f'JointData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* start_pc = {fmt_member(self.start_pc, indent+1)}'
		s += f'\n	* joint_count = {fmt_member(self.joint_count, indent+1)}'
		s += f'\n	* count_0 = {fmt_member(self.count_0, indent+1)}'
		s += f'\n	* count_1 = {fmt_member(self.count_1, indent+1)}'
		s += f'\n	* count_2 = {fmt_member(self.count_2, indent+1)}'
		s += f'\n	* zeros_extra = {fmt_member(self.zeros_extra, indent+1)}'
		s += f'\n	* namespace_length = {fmt_member(self.namespace_length, indent+1)}'
		s += f'\n	* zeros_0 = {fmt_member(self.zeros_0, indent+1)}'
		s += f'\n	* pc_count = {fmt_member(self.pc_count, indent+1)}'
		s += f'\n	* zeros_1 = {fmt_member(self.zeros_1, indent+1)}'
		s += f'\n	* extra_zeros_pc = {fmt_member(self.extra_zeros_pc, indent+1)}'
		s += f'\n	* ones = {fmt_member(self.ones, indent+1)}'
		s += f'\n	* bone_count = {fmt_member(self.bone_count, indent+1)}'
		s += f'\n	* joint_entry_count = {fmt_member(self.joint_entry_count, indent+1)}'
		s += f'\n	* zeros_2 = {fmt_member(self.zeros_2, indent+1)}'
		s += f'\n	* joint_transforms = {fmt_member(self.joint_transforms, indent+1)}'
		s += f'\n	* zeros_3 = {fmt_member(self.zeros_3, indent+1)}'
		s += f'\n	* unknown_listc = {fmt_member(self.unknown_listc, indent+1)}'
		s += f'\n	* first_list = {fmt_member(self.first_list, indent+1)}'
		s += f'\n	* short_list = {fmt_member(self.short_list, indent+1)}'
		s += f'\n	* long_list = {fmt_member(self.long_list, indent+1)}'
		s += f'\n	* joint_infos = {fmt_member(self.joint_infos, indent+1)}'
		s += f'\n	* pc_floats = {fmt_member(self.pc_floats, indent+1)}'
		s += f'\n	* joint_indices = {fmt_member(self.joint_indices, indent+1)}'
		s += f'\n	* bone_indices = {fmt_member(self.bone_indices, indent+1)}'
		s += f'\n	* joint_names = {fmt_member(self.joint_names, indent+1)}'
		s += f'\n	* joint_names_padding = {fmt_member(self.joint_names_padding, indent+1)}'
		s += f'\n	* joint_infos = {fmt_member(self.joint_infos, indent+1)}'
		s += f'\n	* hitcheck_reader = {fmt_member(self.hitcheck_reader, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
