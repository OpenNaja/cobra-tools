import typing
from generated.array import Array
from generated.formats.manis.compound.ManiInfo import ManiInfo
from generated.formats.manis.compound.SizedStrData import SizedStrData


class InfoHeader:

	"""
	Custom header struct
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 'MANI'
		self.magic = Array()
		self.version = 0
		self.flag_2 = 0
		self.mani_count = 0
		self.names = Array()
		self.header = SizedStrData()
		self.mani_infos = Array()
		self.bone_hashes = Array()
		self.bone_names = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.magic.read(stream, 'Byte', 4, None)
		self.version = stream.read_uint()
		stream.version = self.version
		self.flag_2 = stream.read_uint()
		self.mani_count = stream.read_uint()
		self.names.read(stream, 'ZString', self.mani_count, None)
		self.header = stream.read_type(SizedStrData)
		self.mani_infos.read(stream, ManiInfo, self.mani_count, None)
		self.bone_hashes.read(stream, 'Uint', int(self.header.hash_block_size / 4), None)
		self.bone_names.read(stream, 'ZString', int(self.header.hash_block_size / 4), None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		self.magic.write(stream, 'Byte', 4, None)
		stream.write_uint(self.version)
		stream.version = self.version
		stream.write_uint(self.flag_2)
		stream.write_uint(self.mani_count)
		self.names.write(stream, 'ZString', self.mani_count, None)
		stream.write_type(self.header)
		self.mani_infos.write(stream, ManiInfo, self.mani_count, None)
		self.bone_hashes.write(stream, 'Uint', int(self.header.hash_block_size / 4), None)
		self.bone_names.write(stream, 'ZString', int(self.header.hash_block_size / 4), None)

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
