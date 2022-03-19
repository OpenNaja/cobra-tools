from source.formats.base.basic import fmt_member
from generated.context import ContextReference
from generated.formats.dds.bitstruct.PixelFormatFlags import PixelFormatFlags
from generated.formats.dds.enum.FourCC import FourCC


class PixelFormat:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# Always 32.
		self.size = 32

		# Non-zero for DX9, zero for DX10.
		self.flags = PixelFormatFlags(self.context, 0, None)

		# Determines compression type. Zero means no compression.
		self.four_c_c = FourCC(self.context, 0, None)

		# For non-compressed types, this is either 24 or 32 depending on whether there is an alpha channel. For compressed types, this describes the number of bits per block, which can be either 256 or 512.
		self.bit_count = 0

		# For non-compressed types, this determines the red mask. Usually 0x00FF0000. Is zero for compressed textures.
		self.r_mask = 0

		# For non-compressed types, this determines
		# the green mask. Usually 0x0000FF00. Is zero for compressed textures.
		self.g_mask = 0

		# For non-compressed types, this determines
		# the blue mask. Usually 0x00FF0000. Is zero for compressed textures.
		self.b_mask = 0

		# For non-compressed types, this determines
		# the alpha mask. Usually 0x00000000 if there is no alpha channel and 0xFF000000 if there is an alpha channel. Is zero for compressed textures.
		self.a_mask = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.size = 32
		self.flags = PixelFormatFlags(self.context, 0, None)
		self.four_c_c = FourCC(self.context, 0, None)
		self.bit_count = 0
		self.r_mask = 0
		self.g_mask = 0
		self.b_mask = 0
		self.a_mask = 0

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
		instance.size = stream.read_uint()
		instance.flags = PixelFormatFlags.from_stream(stream, instance.context, 0, None)
		instance.four_c_c = FourCC.from_value(stream.read_uint())
		instance.bit_count = stream.read_uint()
		instance.r_mask = stream.read_uint()
		instance.g_mask = stream.read_uint()
		instance.b_mask = stream.read_uint()
		instance.a_mask = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.size)
		PixelFormatFlags.to_stream(stream, instance.flags)
		stream.write_uint(instance.four_c_c.value)
		stream.write_uint(instance.bit_count)
		stream.write_uint(instance.r_mask)
		stream.write_uint(instance.g_mask)
		stream.write_uint(instance.b_mask)
		stream.write_uint(instance.a_mask)

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

	def get_info_str(self, indent=0):
		return f'PixelFormat [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* size = {fmt_member(self.size, indent+1)}'
		s += f'\n	* flags = {fmt_member(self.flags, indent+1)}'
		s += f'\n	* four_c_c = {fmt_member(self.four_c_c, indent+1)}'
		s += f'\n	* bit_count = {fmt_member(self.bit_count, indent+1)}'
		s += f'\n	* r_mask = {fmt_member(self.r_mask, indent+1)}'
		s += f'\n	* g_mask = {fmt_member(self.g_mask, indent+1)}'
		s += f'\n	* b_mask = {fmt_member(self.b_mask, indent+1)}'
		s += f'\n	* a_mask = {fmt_member(self.a_mask, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
