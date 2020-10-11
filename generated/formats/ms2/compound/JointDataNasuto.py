import typing
from generated.formats.ms2.compound.JointCompound import JointCompound
from generated.formats.ms2.compound.JointEntry import JointEntry
from generated.formats.ms2.compound.JointInfo import JointInfo
from generated.formats.ms2.compound.ListCEntry import ListCEntry
from generated.formats.ms2.compound.NasutoJointEntry import NasutoJointEntry
from generated.formats.ms2.compound.ZStringBuffer import ZStringBuffer


class JointDataNasuto:

	# variable
	joint_count: int

	# 0
	unknown_1: int

	# 0
	unknown_2: int

	# 0
	unknown_3: int

	# usually fairly big nr, 500ish
	unknown_4: int
	unknown_list: typing.List[NasutoJointEntry]

	# 0
	zero: int

	# small number
	count_0: int

	# small number
	count_1: int
	joint_compound: JointCompound
	unknown_lista: typing.List[JointEntry]
	unknown_listb: typing.List[int]
	unknown_listc: typing.List[ListCEntry]

	# 3
	d: int

	# 2
	e: int

	# velo01male
	undecoded_floats: typing.List[float]

	# index
	indices: typing.List[int]

	# index or -1
	indices_2: typing.List[int]
	joint_names: ZStringBuffer
	joint_names_padding: typing.List[int]
	joint_info_list: typing.List[JointInfo]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.joint_count = 0
		self.unknown_1 = 0
		self.unknown_2 = 0
		self.unknown_3 = 0
		self.unknown_4 = 0
		self.unknown_list = []
		self.zero = 0
		self.count_0 = 0
		self.count_1 = 0
		self.joint_compound = JointCompound()
		self.unknown_lista = []
		self.unknown_listb = []
		self.unknown_listc = []
		self.d = 0
		self.e = 0
		self.undecoded_floats = []
		self.indices = []
		self.indices_2 = []
		self.joint_names = ZStringBuffer()
		self.joint_names_padding = []
		self.joint_info_list = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.joint_count = stream.read_uint()
		self.unknown_1 = stream.read_uint()
		self.unknown_2 = stream.read_uint()
		self.unknown_3 = stream.read_uint()
		self.unknown_4 = stream.read_uint()
		self.unknown_list = [stream.read_type(NasutoJointEntry) for _ in range(self.joint_count)]
		self.zero = stream.read_uint()
		self.count_0 = stream.read_uint()
		self.count_1 = stream.read_uint()
		self.joint_compound = stream.read_type(JointCompound)
		self.unknown_lista = [stream.read_type(JointEntry) for _ in range(self.arg)]
		self.unknown_listb = [stream.read_uint64() for _ in range(self.arg)]
		self.unknown_listc = [stream.read_type(ListCEntry) for _ in range(self.arg)]
		self.d = stream.read_ushort()
		self.e = stream.read_ushort()
		self.undecoded_floats = [stream.read_float() for _ in range(917)]
		self.indices = [stream.read_uint() for _ in range(self.arg)]
		self.indices_2 = [stream.read_int() for _ in range(self.joint_compound.unknown_8)]
		self.joint_names = stream.read_type(ZStringBuffer, (self.joint_compound.namespace_length,))
		self.joint_names_padding = [stream.read_byte() for _ in range((8 - (self.joint_compound.namespace_length % 8)) % 8)]
		self.joint_info_list = [stream.read_type(JointInfo) for _ in range(self.arg)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.joint_count)
		stream.write_uint(self.unknown_1)
		stream.write_uint(self.unknown_2)
		stream.write_uint(self.unknown_3)
		stream.write_uint(self.unknown_4)
		for item in self.unknown_list: stream.write_type(item)
		stream.write_uint(self.zero)
		stream.write_uint(self.count_0)
		stream.write_uint(self.count_1)
		stream.write_type(self.joint_compound)
		for item in self.unknown_lista: stream.write_type(item)
		for item in self.unknown_listb: stream.write_uint64(item)
		for item in self.unknown_listc: stream.write_type(item)
		stream.write_ushort(self.d)
		stream.write_ushort(self.e)
		for item in self.undecoded_floats: stream.write_float(item)
		for item in self.indices: stream.write_uint(item)
		for item in self.indices_2: stream.write_int(item)
		stream.write_type(self.joint_names)
		for item in self.joint_names_padding: stream.write_byte(item)
		for item in self.joint_info_list: stream.write_type(item)

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
