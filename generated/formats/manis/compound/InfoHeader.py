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

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.mani_count = 0
		self.names = Array((self.mani_count,), ZString, self.context, 0, None)
		self.header = SizedStrData(self.context, 0, None)
		self.mani_infos = Array((self.mani_count,), ManiInfo, self.context, 0, None)
		self.bone_hashes = numpy.zeros((int(self.header.hash_block_size / 4),), dtype=numpy.dtype('uint32'))
		self.bone_names = Array((int(self.header.hash_block_size / 4),), ZString, self.context, 0, None)

		# ?
		self.bone_pad = PadAlign(self.context, 4, bone names)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.mani_count = 0
		self.names = Array((self.mani_count,), ZString, self.context, 0, None)
		self.header = SizedStrData(self.context, 0, None)
		self.mani_infos = Array((self.mani_count,), ManiInfo, self.context, 0, None)
		self.bone_hashes = numpy.zeros((int(self.header.hash_block_size / 4),), dtype=numpy.dtype('uint32'))
		self.bone_names = Array((int(self.header.hash_block_size / 4),), ZString, self.context, 0, None)
		self.bone_pad = PadAlign(self.context, 4, bone names)

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
		super().read_fields(stream, instance)
		instance.mani_count = stream.read_uint()
		instance.names = stream.read_zstrings((instance.mani_count,))
		instance.header = SizedStrData.from_stream(stream, instance.context, 0, None)
		instance.mani_infos = Array.from_stream(stream, (instance.mani_count,), ManiInfo, instance.context, 0, None)
		instance.bone_hashes = stream.read_uints((int(instance.header.hash_block_size / 4),))
		instance.bone_names = stream.read_zstrings((int(instance.header.hash_block_size / 4),))
		instance.bone_pad = PadAlign.from_stream(stream, instance.context, 4, bone names)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.mani_count)
		stream.write_zstrings(instance.names)
		SizedStrData.to_stream(stream, instance.header)
		Array.to_stream(stream, instance.mani_infos, (instance.mani_count,),ManiInfo, instance.context, 0, None)
		stream.write_uints(instance.bone_hashes)
		stream.write_zstrings(instance.bone_names)
		PadAlign.to_stream(stream, instance.bone_pad)

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
