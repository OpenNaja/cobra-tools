from generated.formats.base.basic import fmt_member
from generated.formats.base.basic import Int
from generated.formats.base.basic import Short
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class TexBuffer(MemStruct):

	"""
	Describes one buffer of a tex / texturestream file.
	24 bytes per texture buffer
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# byte offset in the combined buffer
		self.offset = 0

		# byte size of this tex buffer
		self.size = 0

		# index of first mip used in this buffer
		self.first_mip = 0

		# amount of mip levels included in this buffer
		self.mip_count = 0
		self.padding_0 = 0
		self.padding_1 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.offset = 0
		self.size = 0
		self.first_mip = 0
		self.mip_count = 0
		self.padding_0 = 0
		self.padding_1 = 0

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
		instance.offset = stream.read_uint64()
		instance.size = stream.read_uint64()
		instance.first_mip = stream.read_ubyte()
		instance.mip_count = stream.read_ubyte()
		instance.padding_0 = stream.read_short()
		instance.padding_1 = stream.read_int()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64(instance.offset)
		stream.write_uint64(instance.size)
		stream.write_ubyte(instance.first_mip)
		stream.write_ubyte(instance.mip_count)
		stream.write_short(instance.padding_0)
		stream.write_int(instance.padding_1)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('offset', Uint64, (0, None))
		yield ('size', Uint64, (0, None))
		yield ('first_mip', Ubyte, (0, None))
		yield ('mip_count', Ubyte, (0, None))
		yield ('padding_0', Short, (0, None))
		yield ('padding_1', Int, (0, None))

	def get_info_str(self, indent=0):
		return f'TexBuffer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* size = {fmt_member(self.size, indent+1)}'
		s += f'\n	* first_mip = {fmt_member(self.first_mip, indent+1)}'
		s += f'\n	* mip_count = {fmt_member(self.mip_count, indent+1)}'
		s += f'\n	* padding_0 = {fmt_member(self.padding_0, indent+1)}'
		s += f'\n	* padding_1 = {fmt_member(self.padding_1, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
