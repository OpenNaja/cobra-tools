import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.HitCheckEntry import HitCheckEntry
from generated.formats.ms2.compound.JointEntry import JointEntry
from generated.formats.ms2.compound.JointInfo import JointInfo
from generated.formats.ms2.compound.ListCEntry import ListCEntry
from generated.formats.ms2.compound.ListFirst import ListFirst
from generated.formats.ms2.compound.ListLong import ListLong
from generated.formats.ms2.compound.ListShort import ListShort
from generated.formats.ms2.compound.PcFFCounter import PcFFCounter
from generated.formats.ms2.compound.SmartPadding import SmartPadding
from generated.formats.ovl_base.compound.ZStringBuffer import ZStringBuffer


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

		# A7 2D A8 10   00 00 00 00, since ms_2_version 51
		self.new_extra = numpy.zeros((2,), dtype=numpy.dtype('uint32'))

		# repeat
		self.joint_count = 0

		# small number
		self.count_0 = 0

		# small number
		self.count_1 = 0

		# small number
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
		self.unknown_listc = Array((self.joint_count,), ListCEntry, self.context, 0, None)

		# used by ptero, 16 bytes per entry
		self.first_list = Array((self.count_0,), ListFirst, self.context, 0, None)
		self.short_list = Array((self.count_1,), ListShort, self.context, 0, None)
		self.long_list = Array((self.count_2,), ListLong, self.context, 0, None)

		# ?
		self.pc_ffs = PcFFCounter(self.context, 0, None)

		# 1FAA FFAAFF00 000000
		self.pc_bytes = numpy.zeros((9,), dtype=numpy.dtype('int8'))

		# counts hitchecks for pz
		self.pc_hitcheck_count = 0

		# 0
		self.pc_zero_0 = 0

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

		# includes name ptrs, some flags, and the hitchecks
		self.joint_info_list = Array((self.joint_count,), JointInfo, self.context, 0, None)

		# bare hitchecks
		self.hitchecks_pc = Array((self.pc_hitcheck_count,), HitCheckEntry, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if self.context.user_version.is_jwe and (self.context.version == 20):
			self.new_extra = numpy.zeros((2,), dtype=numpy.dtype('uint32'))
		self.joint_count = 0
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		if self.context.version == 18:
			self.zeros_extra = numpy.zeros((2,), dtype=numpy.dtype('uint32'))
		self.namespace_length = 0
		self.zeros_0 = numpy.zeros((5,), dtype=numpy.dtype('uint32'))
		self.pc_count = 0
		self.zeros_1 = numpy.zeros((7,), dtype=numpy.dtype('uint32'))
		if self.context.version == 18:
			self.extra_zeros_pc = numpy.zeros((4,), dtype=numpy.dtype('uint32'))
		self.ones = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		self.bone_count = 0
		self.joint_entry_count = 0
		self.zeros_2 = numpy.zeros((4,), dtype=numpy.dtype('uint32'))
		self.joint_transforms = Array((self.joint_count,), JointEntry, self.context, 0, None)
		if not (self.context.version == 18):
			self.zeros_3 = numpy.zeros((self.joint_count,), dtype=numpy.dtype('uint64'))
		if not (self.context.version == 18):
			self.unknown_listc = Array((self.joint_count,), ListCEntry, self.context, 0, None)
		if not (self.context.version == 18):
			self.first_list = Array((self.count_0,), ListFirst, self.context, 0, None)
		if not (self.context.version == 18):
			self.short_list = Array((self.count_1,), ListShort, self.context, 0, None)
		if not (self.context.version == 18):
			self.long_list = Array((self.count_2,), ListLong, self.context, 0, None)
		if self.context.version == 18:
			self.pc_ffs = PcFFCounter(self.context, 0, None)
		if self.context.version == 18:
			self.pc_bytes = numpy.zeros((9,), dtype=numpy.dtype('int8'))
		if self.context.version == 18:
			self.pc_hitcheck_count = 0
		if self.context.version == 18:
			self.pc_zero_0 = 0
		if self.context.version == 18:
			self.pc_floats = numpy.zeros((self.pc_count, 10,), dtype=numpy.dtype('float32'))
		self.joint_indices = numpy.zeros((self.joint_count,), dtype=numpy.dtype('int32'))
		self.bone_indices = numpy.zeros((self.bone_count,), dtype=numpy.dtype('int32'))
		self.joint_names = ZStringBuffer(self.context, self.namespace_length, None)
		self.joint_names_padding = SmartPadding(self.context, 0, None)
		if not (self.context.version == 18):
			self.joint_info_list = Array((self.joint_count,), JointInfo, self.context, 0, None)
		if self.context.version == 18:
			self.hitchecks_pc = Array((self.pc_hitcheck_count,), HitCheckEntry, self.context, 0, None)

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
		if instance.context.user_version.is_jwe and (instance.context.version == 20):
			instance.new_extra = stream.read_uints((2,))
		instance.joint_count = stream.read_uint()
		instance.count_0 = stream.read_uint()
		instance.count_1 = stream.read_uint()
		instance.count_2 = stream.read_uint()
		if instance.context.version == 18:
			instance.zeros_extra = stream.read_uints((2,))
		instance.namespace_length = stream.read_uint()
		instance.zeros_0 = stream.read_uints((5,))
		instance.pc_count = stream.read_uint()
		instance.zeros_1 = stream.read_uints((7,))
		if instance.context.version == 18:
			instance.extra_zeros_pc = stream.read_uints((4,))
		instance.ones = stream.read_uint64s((2,))
		instance.bone_count = stream.read_uint()
		instance.joint_entry_count = stream.read_uint()
		instance.zeros_2 = stream.read_uints((4,))
		instance.joint_transforms = Array.from_stream(stream, (instance.joint_count,), JointEntry, instance.context, 0, None)
		if not (instance.context.version == 18):
			instance.zeros_3 = stream.read_uint64s((instance.joint_count,))
			instance.unknown_listc = Array.from_stream(stream, (instance.joint_count,), ListCEntry, instance.context, 0, None)
		if not (instance.context.version == 18):
			instance.first_list = Array.from_stream(stream, (instance.count_0,), ListFirst, instance.context, 0, None)
			instance.short_list = Array.from_stream(stream, (instance.count_1,), ListShort, instance.context, 0, None)
		if not (instance.context.version == 18):
			instance.long_list = Array.from_stream(stream, (instance.count_2,), ListLong, instance.context, 0, None)
		if instance.context.version == 18:
			instance.pc_ffs = PcFFCounter.from_stream(stream, instance.context, 0, None)
			instance.pc_bytes = stream.read_bytes((9,))
		if instance.context.version == 18:
			instance.pc_hitcheck_count = stream.read_uint64()
			instance.pc_zero_0 = stream.read_uint64()
		if instance.context.version == 18:
			instance.pc_floats = stream.read_floats((instance.pc_count, 10,))
		instance.joint_indices = stream.read_ints((instance.joint_count,))
		instance.bone_indices = stream.read_ints((instance.bone_count,))
		instance.joint_names = ZStringBuffer.from_stream(stream, instance.context, instance.namespace_length, None)
		instance.joint_names_padding = SmartPadding.from_stream(stream, instance.context, 0, None)
		if not (instance.context.version == 18):
			instance.joint_info_list = Array.from_stream(stream, (instance.joint_count,), JointInfo, instance.context, 0, None)
		if instance.context.version == 18:
			instance.hitchecks_pc = Array.from_stream(stream, (instance.pc_hitcheck_count,), HitCheckEntry, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		if instance.context.user_version.is_jwe and (instance.context.version == 20):
			stream.write_uints(instance.new_extra)
		stream.write_uint(instance.joint_count)
		stream.write_uint(instance.count_0)
		stream.write_uint(instance.count_1)
		stream.write_uint(instance.count_2)
		if instance.context.version == 18:
			stream.write_uints(instance.zeros_extra)
		stream.write_uint(instance.namespace_length)
		stream.write_uints(instance.zeros_0)
		stream.write_uint(instance.pc_count)
		stream.write_uints(instance.zeros_1)
		if instance.context.version == 18:
			stream.write_uints(instance.extra_zeros_pc)
		stream.write_uint64s(instance.ones)
		stream.write_uint(instance.bone_count)
		stream.write_uint(instance.joint_entry_count)
		stream.write_uints(instance.zeros_2)
		Array.to_stream(stream, instance.joint_transforms, (instance.joint_count,),JointEntry, instance.context, 0, None)
		if not (instance.context.version == 18):
			stream.write_uint64s(instance.zeros_3)
			Array.to_stream(stream, instance.unknown_listc, (instance.joint_count,),ListCEntry, instance.context, 0, None)
		if not (instance.context.version == 18):
			Array.to_stream(stream, instance.first_list, (instance.count_0,),ListFirst, instance.context, 0, None)
			Array.to_stream(stream, instance.short_list, (instance.count_1,),ListShort, instance.context, 0, None)
		if not (instance.context.version == 18):
			Array.to_stream(stream, instance.long_list, (instance.count_2,),ListLong, instance.context, 0, None)
		if instance.context.version == 18:
			PcFFCounter.to_stream(stream, instance.pc_ffs)
			stream.write_bytes(instance.pc_bytes)
		if instance.context.version == 18:
			stream.write_uint64(instance.pc_hitcheck_count)
			stream.write_uint64(instance.pc_zero_0)
		if instance.context.version == 18:
			stream.write_floats(instance.pc_floats)
		stream.write_ints(instance.joint_indices)
		stream.write_ints(instance.bone_indices)
		ZStringBuffer.to_stream(stream, instance.joint_names)
		SmartPadding.to_stream(stream, instance.joint_names_padding)
		if not (instance.context.version == 18):
			Array.to_stream(stream, instance.joint_info_list, (instance.joint_count,),JointInfo, instance.context, 0, None)
		if instance.context.version == 18:
			Array.to_stream(stream, instance.hitchecks_pc, (instance.pc_hitcheck_count,),HitCheckEntry, instance.context, 0, None)

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
		return f'JointData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* new_extra = {self.new_extra.__repr__()}'
		s += f'\n	* joint_count = {self.joint_count.__repr__()}'
		s += f'\n	* count_0 = {self.count_0.__repr__()}'
		s += f'\n	* count_1 = {self.count_1.__repr__()}'
		s += f'\n	* count_2 = {self.count_2.__repr__()}'
		s += f'\n	* zeros_extra = {self.zeros_extra.__repr__()}'
		s += f'\n	* namespace_length = {self.namespace_length.__repr__()}'
		s += f'\n	* zeros_0 = {self.zeros_0.__repr__()}'
		s += f'\n	* pc_count = {self.pc_count.__repr__()}'
		s += f'\n	* zeros_1 = {self.zeros_1.__repr__()}'
		s += f'\n	* extra_zeros_pc = {self.extra_zeros_pc.__repr__()}'
		s += f'\n	* ones = {self.ones.__repr__()}'
		s += f'\n	* bone_count = {self.bone_count.__repr__()}'
		s += f'\n	* joint_entry_count = {self.joint_entry_count.__repr__()}'
		s += f'\n	* zeros_2 = {self.zeros_2.__repr__()}'
		s += f'\n	* joint_transforms = {self.joint_transforms.__repr__()}'
		s += f'\n	* zeros_3 = {self.zeros_3.__repr__()}'
		s += f'\n	* unknown_listc = {self.unknown_listc.__repr__()}'
		s += f'\n	* first_list = {self.first_list.__repr__()}'
		s += f'\n	* short_list = {self.short_list.__repr__()}'
		s += f'\n	* long_list = {self.long_list.__repr__()}'
		s += f'\n	* pc_ffs = {self.pc_ffs.__repr__()}'
		s += f'\n	* pc_bytes = {self.pc_bytes.__repr__()}'
		s += f'\n	* pc_hitcheck_count = {self.pc_hitcheck_count.__repr__()}'
		s += f'\n	* pc_zero_0 = {self.pc_zero_0.__repr__()}'
		s += f'\n	* pc_floats = {self.pc_floats.__repr__()}'
		s += f'\n	* joint_indices = {self.joint_indices.__repr__()}'
		s += f'\n	* bone_indices = {self.bone_indices.__repr__()}'
		s += f'\n	* joint_names = {self.joint_names.__repr__()}'
		s += f'\n	* joint_names_padding = {self.joint_names_padding.__repr__()}'
		s += f'\n	* joint_info_list = {self.joint_info_list.__repr__()}'
		s += f'\n	* hitchecks_pc = {self.hitchecks_pc.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
