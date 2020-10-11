import typing
from generated.formats.manis.compound.ManiInfo import ManiInfo
from generated.formats.manis.compound.SizedStrData import SizedStrData


class InfoHeader:

	"""
	Custom header struct
	"""

	# 'MANI'
	magic: typing.List[int]
	version: int
	flag_2: int
	mani_count: int
	names: typing.List[str]
	header: SizedStrData
	mani_infos: typing.List[ManiInfo]
	bone_hashes: typing.List[int]
	bone_names: typing.List[str]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.magic = []
		self.version = 0
		self.flag_2 = 0
		self.mani_count = 0
		self.names = []
		self.header = SizedStrData()
		self.mani_infos = []
		self.bone_hashes = []
		self.bone_names = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.magic = [stream.read_byte() for _ in range(4)]
		self.version = stream.read_uint()
		stream.version = self.version
		self.flag_2 = stream.read_uint()
		self.mani_count = stream.read_uint()
		self.names = [stream.read_zstring() for _ in range(self.mani_count)]
		self.header = stream.read_type(SizedStrData)
		self.mani_infos = [stream.read_type(ManiInfo) for _ in range(self.mani_count)]
		self.bone_hashes = [stream.read_uint() for _ in range(int(self.header.hash_block_size / 4))]
		self.bone_names = [stream.read_zstring() for _ in range(int(self.header.hash_block_size / 4))]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		for item in self.magic: stream.write_byte(item)
		stream.write_uint(self.version)
		stream.version = self.version
		stream.write_uint(self.flag_2)
		stream.write_uint(self.mani_count)
		for item in self.names: stream.write_zstring(item)
		stream.write_type(self.header)
		for item in self.mani_infos: stream.write_type(item)
		for item in self.bone_hashes: stream.write_uint(item)
		for item in self.bone_names: stream.write_zstring(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'InfoHeader [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* magic = ' + self.magic.__repr__()
		s += '\n	* version = ' + self.version.__repr__()
		s += '\n	* flag_2 = ' + self.flag_2.__repr__()
		s += '\n	* mani_count = ' + self.mani_count.__repr__()
		s += '\n	* names = ' + self.names.__repr__()
		s += '\n	* header = ' + self.header.__repr__()
		s += '\n	* mani_infos = ' + self.mani_infos.__repr__()
		s += '\n	* bone_hashes = ' + self.bone_hashes.__repr__()
		s += '\n	* bone_names = ' + self.bone_names.__repr__()
		s += '\n'
		return s
