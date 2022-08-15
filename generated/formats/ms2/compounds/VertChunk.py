import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.ms2.bitfields.WeightsFlag import WeightsFlag


class VertChunk(BaseStruct):

	"""
	JWE2 Biosyn: 16 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.flags = numpy.zeros((4,), dtype=numpy.dtype('uint8'))

		# scale: pack_base / 512, also added as offset
		self.pack_base = 0.0

		# byte offset from start of vert buffer in bytes
		self.vertex_offset = 0
		self.vertex_count = 0

		# determines if weights are used by this chunk
		self.weights_flag = WeightsFlag(self.context, 0, None)
		self.zero = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.flags = numpy.zeros((4,), dtype=numpy.dtype('uint8'))
		self.pack_base = 0.0
		self.vertex_offset = 0
		self.vertex_count = 0
		self.weights_flag = WeightsFlag(self.context, 0, None)
		self.zero = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.flags = Array.from_stream(stream, instance.context, 0, None, (4,), Ubyte)
		instance.pack_base = Float.from_stream(stream, instance.context, 0, None)
		instance.vertex_offset = Uint.from_stream(stream, instance.context, 0, None)
		instance.vertex_count = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.weights_flag = WeightsFlag.from_stream(stream, instance.context, 0, None)
		instance.zero = Ubyte.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_ubytes(instance.flags)
		stream.write_float(instance.pack_base)
		stream.write_uint(instance.vertex_offset)
		stream.write_ubyte(instance.vertex_count)
		WeightsFlag.to_stream(stream, instance.weights_flag)
		stream.write_ubyte(instance.zero)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'flags', Array, ((4,), Ubyte, 0, None)
		yield 'pack_base', Float, (0, None)
		yield 'vertex_offset', Uint, (0, None)
		yield 'vertex_count', Ubyte, (0, None)
		yield 'weights_flag', WeightsFlag, (0, None)
		yield 'zero', Ubyte, (0, None)

	def get_info_str(self, indent=0):
		return f'VertChunk [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* flags = {self.fmt_member(self.flags, indent+1)}'
		s += f'\n	* pack_base = {self.fmt_member(self.pack_base, indent+1)}'
		s += f'\n	* vertex_offset = {self.fmt_member(self.vertex_offset, indent+1)}'
		s += f'\n	* vertex_count = {self.fmt_member(self.vertex_count, indent+1)}'
		s += f'\n	* weights_flag = {self.fmt_member(self.weights_flag, indent+1)}'
		s += f'\n	* zero = {self.fmt_member(self.zero, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
