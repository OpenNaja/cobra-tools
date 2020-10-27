import typing
from generated.array import Array
from generated.formats.ms2.compound.JointCompound import JointCompound
from generated.formats.ms2.compound.JointEntry import JointEntry
from generated.formats.ms2.compound.JointInfo import JointInfo
from generated.formats.ms2.compound.ListCEntry import ListCEntry
from generated.formats.ms2.compound.NasutoJointEntry import NasutoJointEntry
from generated.formats.ms2.compound.ZStringBuffer import ZStringBuffer


class JointDataNasuto:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# variable
		self.joint_count = 0

		# 0
		self.unknown_1 = 0

		# 0
		self.unknown_2 = 0

		# 0
		self.unknown_3 = 0

		# usually fairly big nr, 500ish
		self.unknown_4 = 0
		self.unknown_list = Array()

		# 0
		self.zero = 0

		# small number
		self.count_0 = 0

		# small number
		self.count_1 = 0
		self.joint_compound = JointCompound()
		self.unknown_lista = Array()
		self.unknown_listb = Array()
		self.unknown_listc = Array()

		# 3
		self.d = 0

		# 2
		self.e = 0

		# velo01male
		self.undecoded_floats = Array()

		# index
		self.indices = Array()

		# index or -1
		self.indices_2 = Array()
		self.joint_names = ZStringBuffer()
		self.joint_names_padding = Array()
		self.joint_info_list = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.joint_count = stream.read_uint()
		self.unknown_1 = stream.read_uint()
		self.unknown_2 = stream.read_uint()
		self.unknown_3 = stream.read_uint()
		self.unknown_4 = stream.read_uint()
		self.unknown_list.read(stream, NasutoJointEntry, self.joint_count, None)
		self.zero = stream.read_uint()
		self.count_0 = stream.read_uint()
		self.count_1 = stream.read_uint()
		self.joint_compound = stream.read_type(JointCompound)
		self.unknown_lista.read(stream, JointEntry, self.arg, None)
		self.unknown_listb.read(stream, 'Uint64', self.arg, None)
		self.unknown_listc.read(stream, ListCEntry, self.arg, None)
		self.d = stream.read_ushort()
		self.e = stream.read_ushort()
		self.undecoded_floats.read(stream, 'Float', 917, None)
		self.indices.read(stream, 'Uint', self.arg, None)
		self.indices_2.read(stream, 'Int', self.joint_compound.unknown_8, None)
		self.joint_names = stream.read_type(ZStringBuffer, (self.joint_compound.namespace_length,))
		self.joint_names_padding.read(stream, 'Byte', (8 - (self.joint_compound.namespace_length % 8)) % 8, None)
		self.joint_info_list.read(stream, JointInfo, self.arg, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.joint_count)
		stream.write_uint(self.unknown_1)
		stream.write_uint(self.unknown_2)
		stream.write_uint(self.unknown_3)
		stream.write_uint(self.unknown_4)
		self.unknown_list.write(stream, NasutoJointEntry, self.joint_count, None)
		stream.write_uint(self.zero)
		stream.write_uint(self.count_0)
		stream.write_uint(self.count_1)
		stream.write_type(self.joint_compound)
		self.unknown_lista.write(stream, JointEntry, self.arg, None)
		self.unknown_listb.write(stream, 'Uint64', self.arg, None)
		self.unknown_listc.write(stream, ListCEntry, self.arg, None)
		stream.write_ushort(self.d)
		stream.write_ushort(self.e)
		self.undecoded_floats.write(stream, 'Float', 917, None)
		self.indices.write(stream, 'Uint', self.arg, None)
		self.indices_2.write(stream, 'Int', self.joint_compound.unknown_8, None)
		stream.write_type(self.joint_names)
		self.joint_names_padding.write(stream, 'Byte', (8 - (self.joint_compound.namespace_length % 8)) % 8, None)
		self.joint_info_list.write(stream, JointInfo, self.arg, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'JointDataNasuto [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* joint_count = ' + self.joint_count.__repr__()
		s += '\n	* unknown_1 = ' + self.unknown_1.__repr__()
		s += '\n	* unknown_2 = ' + self.unknown_2.__repr__()
		s += '\n	* unknown_3 = ' + self.unknown_3.__repr__()
		s += '\n	* unknown_4 = ' + self.unknown_4.__repr__()
		s += '\n	* unknown_list = ' + self.unknown_list.__repr__()
		s += '\n	* zero = ' + self.zero.__repr__()
		s += '\n	* count_0 = ' + self.count_0.__repr__()
		s += '\n	* count_1 = ' + self.count_1.__repr__()
		s += '\n	* joint_compound = ' + self.joint_compound.__repr__()
		s += '\n	* unknown_lista = ' + self.unknown_lista.__repr__()
		s += '\n	* unknown_listb = ' + self.unknown_listb.__repr__()
		s += '\n	* unknown_listc = ' + self.unknown_listc.__repr__()
		s += '\n	* d = ' + self.d.__repr__()
		s += '\n	* e = ' + self.e.__repr__()
		s += '\n	* undecoded_floats = ' + self.undecoded_floats.__repr__()
		s += '\n	* indices = ' + self.indices.__repr__()
		s += '\n	* indices_2 = ' + self.indices_2.__repr__()
		s += '\n	* joint_names = ' + self.joint_names.__repr__()
		s += '\n	* joint_names_padding = ' + self.joint_names_padding.__repr__()
		s += '\n	* joint_info_list = ' + self.joint_info_list.__repr__()
		s += '\n'
		return s
