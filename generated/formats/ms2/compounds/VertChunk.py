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

	__name__ = 'VertChunk'

	_import_path = 'generated.formats.ms2.compounds.VertChunk'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.flags = Array(self.context, 0, None, (0,), Ubyte)

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
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'flags', Array, (0, None, (4,), Ubyte), (False, None)
		yield 'pack_base', Float, (0, None), (False, None)
		yield 'vertex_offset', Uint, (0, None), (False, None)
		yield 'vertex_count', Ubyte, (0, None), (False, None)
		yield 'weights_flag', WeightsFlag, (0, None), (False, None)
		yield 'zero', Ubyte, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'VertChunk [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
