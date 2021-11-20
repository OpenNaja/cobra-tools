import numpy
from generated.array import Array
from generated.formats.base.basic import ZString
from generated.formats.manis.compound.ManiInfo import ManiInfo
from generated.formats.manis.compound.PadAlign import PadAlign
from generated.formats.manis.compound.SizedStrData import SizedStrData
from generated.formats.ovl_base.compound.GenericHeader import GenericHeader


class InfoHeader(GenericHeader):

	"""
	Custom header struct
	"""

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.mani_count = 0
		self.names = Array((self.mani_count), ZString, self.context, None, None)
		self.header = SizedStrData(self.context, None, None)
		self.mani_infos = Array((self.mani_count), ManiInfo, self.context, None, None)
		self.bone_hashes = numpy.zeros((int(self.header.hash_block_size / 4)), dtype=numpy.dtype('uint32'))
		self.bone_names = Array((int(self.header.hash_block_size / 4)), ZString, self.context, None, None)

		# ?
		self.bone_pad = PadAlign(self.context, self.bone_names, 4)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.mani_count = 0
		self.names = Array((self.mani_count), ZString, self.context, None, None)
		self.header = SizedStrData(self.context, None, None)
		self.mani_infos = Array((self.mani_count), ManiInfo, self.context, None, None)
		self.bone_hashes = numpy.zeros((int(self.header.hash_block_size / 4)), dtype=numpy.dtype('uint32'))
		self.bone_names = Array((int(self.header.hash_block_size / 4)), ZString, self.context, None, None)
		self.bone_pad = PadAlign(self.context, self.bone_names, 4)

	def read(self, stream):
		super().read(stream)
		self.mani_count = stream.read_uint()
		self.names = stream.read_zstrings((self.mani_count))
		self.header = stream.read_type(SizedStrData, (self.context, None, None))
		self.mani_infos.read(stream, ManiInfo, self.mani_count, None)
		self.bone_hashes = stream.read_uints((int(self.header.hash_block_size / 4)))
		self.bone_names = stream.read_zstrings((int(self.header.hash_block_size / 4)))
		self.bone_pad = stream.read_type(PadAlign, (self.context, self.bone_names, 4))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		super().write(stream)
		stream.write_uint(self.mani_count)
		stream.write_zstrings(self.names)
		stream.write_type(self.header)
		self.mani_infos.write(stream, ManiInfo, self.mani_count, None)
		stream.write_uints(self.bone_hashes)
		stream.write_zstrings(self.bone_names)
		stream.write_type(self.bone_pad)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'InfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* mani_count = {self.mani_count.__repr__()}'
		s += f'\n	* names = {self.names.__repr__()}'
		s += f'\n	* header = {self.header.__repr__()}'
		s += f'\n	* mani_infos = {self.mani_infos.__repr__()}'
		s += f'\n	* bone_hashes = {self.bone_hashes.__repr__()}'
		s += f'\n	* bone_names = {self.bone_names.__repr__()}'
		s += f'\n	* bone_pad = {self.bone_pad.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
