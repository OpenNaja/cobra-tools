import numpy
import typing
from generated.array import Array
from generated.formats.manis.compound.Buffer1 import Buffer1
from generated.formats.manis.compound.ManiInfo import ManiInfo
from generated.formats.manis.compound.SizedStrData import SizedStrData
from generated.formats.ovl_base.compound.GenericHeader import GenericHeader


class InfoHeader(GenericHeader):

	"""
	Custom header struct
	"""

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		super().__init__(context, arg, template)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.mani_count = 0
		self.names = Array(self.context)
		self.header = SizedStrData(self.context, None, None)
		self.mani_infos = Array(self.context)
		self.name_buffer = Buffer1(self.context, int(self.header.hash_block_size / 4), None)
		self.set_defaults()

	def set_defaults(self):
		self.mani_count = 0
		self.names = Array(self.context)
		self.header = SizedStrData(self.context, None, None)
		self.mani_infos = Array(self.context)
		self.name_buffer = Buffer1(self.context, int(self.header.hash_block_size / 4), None)

	def read(self, stream):
		self.io_start = stream.tell()
		super().read(stream)
		self.mani_count = stream.read_uint()
		self.names = stream.read_zstrings((self.mani_count))
		self.header = stream.read_type(SizedStrData, (self.context, None, None))
		self.mani_infos.read(stream, ManiInfo, self.mani_count, None)
		self.name_buffer = stream.read_type(Buffer1, (self.context, int(self.header.hash_block_size / 4), None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		super().write(stream)
		stream.write_uint(self.mani_count)
		stream.write_zstrings(self.names)
		stream.write_type(self.header)
		self.mani_infos.write(stream, ManiInfo, self.mani_count, None)
		stream.write_type(self.name_buffer)

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
		s += f'\n	* name_buffer = {self.name_buffer.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
