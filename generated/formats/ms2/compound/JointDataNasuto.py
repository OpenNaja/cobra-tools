import typing
from generated.array import Array
from generated.formats.ms2.compound.JointCompound import JointCompound
from generated.formats.ms2.compound.JointEntry import JointEntry
from generated.formats.ms2.compound.JointInfo import JointInfo
from generated.formats.ms2.compound.ListCEntry import ListCEntry
from generated.formats.ms2.compound.ListFirst import ListFirst
from generated.formats.ms2.compound.ListLong import ListLong
from generated.formats.ms2.compound.ListShort import ListShort
from generated.formats.ms2.compound.ZStringBuffer import ZStringBuffer


class JointDataNasuto:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.joint_compound = JointCompound()
		self.unknown_lista = Array()

		# might be pointers
		self.zeros = Array()
		self.unknown_listc = Array()

		# used by ptero, 16 bytes per entry
		self.first_list = Array()
		self.short_list = Array()
		self.long_list = Array()

		# index
		self.joint_indices = Array()

		# index or -1
		self.bone_indices = Array()
		self.joint_names = ZStringBuffer()
		self.joint_names_padding = Array()
		self.joint_info_list = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.joint_compound = stream.read_type(JointCompound)
		self.unknown_lista.read(stream, JointEntry, self.joint_compound.joint_count, None)
		self.zeros = stream.read_uint64s((self.joint_compound.joint_count))
		self.unknown_listc.read(stream, ListCEntry, self.joint_compound.joint_count, None)
		self.first_list.read(stream, ListFirst, self.joint_compound.count_0, None)
		self.short_list.read(stream, ListShort, self.joint_compound.count_1, None)
		self.long_list.read(stream, ListLong, self.joint_compound.count_2, None)
		self.joint_indices = stream.read_ints((self.joint_compound.joint_count))
		self.bone_indices = stream.read_ints((self.joint_compound.bone_count))
		self.joint_names = stream.read_type(ZStringBuffer, (self.joint_compound.namespace_length,))
		self.joint_names_padding = stream.read_bytes(((4 - (self.joint_compound.namespace_length % 8)) % 8))
		self.joint_info_list.read(stream, JointInfo, self.joint_compound.joint_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.joint_compound)
		self.unknown_lista.write(stream, JointEntry, self.joint_compound.joint_count, None)
		stream.write_uint64s(self.zeros)
		self.unknown_listc.write(stream, ListCEntry, self.joint_compound.joint_count, None)
		self.first_list.write(stream, ListFirst, self.joint_compound.count_0, None)
		self.short_list.write(stream, ListShort, self.joint_compound.count_1, None)
		self.long_list.write(stream, ListLong, self.joint_compound.count_2, None)
		stream.write_ints(self.joint_indices)
		stream.write_ints(self.bone_indices)
		stream.write_type(self.joint_names)
		stream.write_bytes(self.joint_names_padding)
		self.joint_info_list.write(stream, JointInfo, self.joint_compound.joint_count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'JointDataNasuto [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* joint_compound = {self.joint_compound.__repr__()}'
		s += f'\n	* unknown_lista = {self.unknown_lista.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* unknown_listc = {self.unknown_listc.__repr__()}'
		s += f'\n	* first_list = {self.first_list.__repr__()}'
		s += f'\n	* short_list = {self.short_list.__repr__()}'
		s += f'\n	* long_list = {self.long_list.__repr__()}'
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
