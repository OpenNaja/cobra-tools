from generated.formats.base.basic import Int
from generated.formats.base.basic import Short
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class TexBuffer(MemStruct):

	"""
	Describes one buffer of a tex / texturestream file.
	24 bytes per texture buffer
	"""

	__name__ = 'TexBuffer'

	_import_path = 'generated.formats.tex.compounds.TexBuffer'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

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
		super().set_defaults()
		self.offset = 0
		self.size = 0
		self.first_mip = 0
		self.mip_count = 0
		self.padding_0 = 0
		self.padding_1 = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.offset = Uint64.from_stream(stream, instance.context, 0, None)
		instance.size = Uint64.from_stream(stream, instance.context, 0, None)
		instance.first_mip = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.mip_count = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.padding_0 = Short.from_stream(stream, instance.context, 0, None)
		instance.padding_1 = Int.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.offset)
		Uint64.to_stream(stream, instance.size)
		Ubyte.to_stream(stream, instance.first_mip)
		Ubyte.to_stream(stream, instance.mip_count)
		Short.to_stream(stream, instance.padding_0)
		Int.to_stream(stream, instance.padding_1)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'offset', Uint64, (0, None), (False, None)
		yield 'size', Uint64, (0, None), (False, None)
		yield 'first_mip', Ubyte, (0, None), (False, None)
		yield 'mip_count', Ubyte, (0, None), (False, None)
		yield 'padding_0', Short, (0, None), (False, None)
		yield 'padding_1', Int, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'TexBuffer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
