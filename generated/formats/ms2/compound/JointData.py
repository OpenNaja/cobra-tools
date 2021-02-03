import typing
from generated.array import Array
from generated.formats.ms2.compound.JointEntry import JointEntry
from generated.formats.ms2.compound.JointInfo import JointInfo
from generated.formats.ms2.compound.ListCEntry import ListCEntry
from generated.formats.ms2.compound.ListFirst import ListFirst
from generated.formats.ms2.compound.ListLong import ListLong
from generated.formats.ms2.compound.ListShort import ListShort
from generated.formats.ms2.compound.PcFFCounter import PcFFCounter
from generated.formats.ms2.compound.SmartPadding import SmartPadding
from generated.formats.ms2.compound.ZStringBuffer import ZStringBuffer


class JointData:

	"""
	appears in dinos and static meshes
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# repeat
		self.joint_count = 0

		# small number
		self.count_0 = 0

		# small number
		self.count_1 = 0

		# small number
		self.count_2 = 0

		# 0s
		self.zeros_extra = Array()
		self.namespace_length = 0

		# 0s
		self.zeros = Array()

		# 0s
		self.zeros = Array()

		# 1, 1
		self.ones = Array()

		# matches bone count from bone info
		self.bone_count = 0

		# 0
		self.joint_entry_count = 0

		# usually 0s
		self.zeros_1 = Array()
		self.unknown_lista = Array()

		# might be pointers
		self.zeros_2 = Array()
		self.unknown_listc = Array()

		# used by ptero, 16 bytes per entry
		self.first_list = Array()
		self.short_list = Array()
		self.long_list = Array()
		self.pc_ffs = Array()

		# index into bone info bones for each joint; bone that the joint is attached to
		self.joint_indices = Array()

		# the inverse of the above; for each bone info bone, index of the corresponding joint or -1 if no joint
		self.bone_indices = Array()
		self.joint_names = ZStringBuffer()
		self.joint_names_padding = SmartPadding()
		self.joint_info_list = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.joint_count = stream.read_uint()
		self.count_0 = stream.read_uint()
		self.count_1 = stream.read_uint()
		self.count_2 = stream.read_uint()
		if stream.version == 18:
			self.zeros_extra = stream.read_uints((2))
		self.namespace_length = stream.read_uint()
		if not (stream.version == 18):
			self.zeros = stream.read_uints((13))
		if stream.version == 18:
			self.zeros = stream.read_uints((17))
		self.ones = stream.read_uint64s((2))
		self.bone_count = stream.read_uint()
		self.joint_entry_count = stream.read_uint()
		self.zeros_1 = stream.read_uints((4))
		self.unknown_lista.read(stream, JointEntry, self.joint_count, None)
		if not (stream.version == 18):
			self.zeros_2 = stream.read_uint64s((self.joint_count))
			self.unknown_listc.read(stream, ListCEntry, self.joint_count, None)
			self.first_list.read(stream, ListFirst, self.count_0, None)
			self.short_list.read(stream, ListShort, self.count_1, None)
			self.long_list.read(stream, ListLong, self.count_2, None)
		if stream.version == 18:
			self.pc_ffs.read(stream, PcFFCounter, self.joint_count, None)
		self.joint_indices = stream.read_ints((self.joint_count))
		self.bone_indices = stream.read_ints((self.bone_count))
		self.joint_names = stream.read_type(ZStringBuffer, (self.namespace_length,))
		self.joint_names_padding = stream.read_type(SmartPadding)
		self.joint_info_list.read(stream, JointInfo, self.joint_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.joint_count)
		stream.write_uint(self.count_0)
		stream.write_uint(self.count_1)
		stream.write_uint(self.count_2)
		if stream.version == 18:
			stream.write_uints(self.zeros_extra)
		stream.write_uint(self.namespace_length)
		if not (stream.version == 18):
			stream.write_uints(self.zeros)
		if stream.version == 18:
			stream.write_uints(self.zeros)
		stream.write_uint64s(self.ones)
		stream.write_uint(self.bone_count)
		stream.write_uint(self.joint_entry_count)
		stream.write_uints(self.zeros_1)
		self.unknown_lista.write(stream, JointEntry, self.joint_count, None)
		if not (stream.version == 18):
			stream.write_uint64s(self.zeros_2)
			self.unknown_listc.write(stream, ListCEntry, self.joint_count, None)
			self.first_list.write(stream, ListFirst, self.count_0, None)
			self.short_list.write(stream, ListShort, self.count_1, None)
			self.long_list.write(stream, ListLong, self.count_2, None)
		if stream.version == 18:
			self.pc_ffs.write(stream, PcFFCounter, self.joint_count, None)
		stream.write_ints(self.joint_indices)
		stream.write_ints(self.bone_indices)
		stream.write_type(self.joint_names)
		stream.write_type(self.joint_names_padding)
		self.joint_info_list.write(stream, JointInfo, self.joint_count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'JointData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* joint_count = {self.joint_count.__repr__()}'
		s += f'\n	* count_0 = {self.count_0.__repr__()}'
		s += f'\n	* count_1 = {self.count_1.__repr__()}'
		s += f'\n	* count_2 = {self.count_2.__repr__()}'
		s += f'\n	* zeros_extra = {self.zeros_extra.__repr__()}'
		s += f'\n	* namespace_length = {self.namespace_length.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* ones = {self.ones.__repr__()}'
		s += f'\n	* bone_count = {self.bone_count.__repr__()}'
		s += f'\n	* joint_entry_count = {self.joint_entry_count.__repr__()}'
		s += f'\n	* zeros_1 = {self.zeros_1.__repr__()}'
		s += f'\n	* unknown_lista = {self.unknown_lista.__repr__()}'
		s += f'\n	* zeros_2 = {self.zeros_2.__repr__()}'
		s += f'\n	* unknown_listc = {self.unknown_listc.__repr__()}'
		s += f'\n	* first_list = {self.first_list.__repr__()}'
		s += f'\n	* short_list = {self.short_list.__repr__()}'
		s += f'\n	* long_list = {self.long_list.__repr__()}'
		s += f'\n	* pc_ffs = {self.pc_ffs.__repr__()}'
		s += f'\n	* joint_indices = {self.joint_indices.__repr__()}'
		s += f'\n	* bone_indices = {self.bone_indices.__repr__()}'
		s += f'\n	* joint_names = {self.joint_names.__repr__()}'
		s += f'\n	* joint_names_padding = {self.joint_names_padding.__repr__()}'
		s += f'\n	* joint_info_list = {self.joint_info_list.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
