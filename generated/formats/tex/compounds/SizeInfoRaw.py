from generated.array import Array
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.tex.compounds.Mipmap import Mipmap


class SizeInfoRaw(MemStruct):

	"""
	Data struct for headers of type 7
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# zero
		self.zero = 0

		# total dds buffer size
		self.data_size = 0

		# x size in pixels
		self.width = 0

		# y size in pixels
		self.height = 0

		# may be depth
		self.depth = 0

		# amount of repeats of the data for each lod
		self.array_size = 0

		# amount of mip map levels
		self.num_mips = 0

		# only found in PZ and JWE2
		self.unk_pz = 0

		# info about mip levels
		self.mip_maps = Array((self.num_mips,), Mipmap, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.zero = 0
		self.data_size = 0
		self.width = 0
		self.height = 0
		self.depth = 0
		self.array_size = 0
		self.num_mips = 0
		if self.context.version >= 20:
			self.unk_pz = 0
		self.mip_maps = Array((self.num_mips,), Mipmap, self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.zero = Uint64.from_stream(stream, instance.context, 0, None)
		instance.data_size = Uint.from_stream(stream, instance.context, 0, None)
		instance.width = Uint.from_stream(stream, instance.context, 0, None)
		instance.height = Uint.from_stream(stream, instance.context, 0, None)
		instance.depth = Uint.from_stream(stream, instance.context, 0, None)
		instance.array_size = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_mips = Uint.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 20:
			instance.unk_pz = Uint64.from_stream(stream, instance.context, 0, None)
		instance.mip_maps = Array.from_stream(stream, instance.context, 0, None, (instance.num_mips,), Mipmap)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.zero)
		Uint.to_stream(stream, instance.data_size)
		Uint.to_stream(stream, instance.width)
		Uint.to_stream(stream, instance.height)
		Uint.to_stream(stream, instance.depth)
		Uint.to_stream(stream, instance.array_size)
		Uint.to_stream(stream, instance.num_mips)
		if instance.context.version >= 20:
			Uint64.to_stream(stream, instance.unk_pz)
		Array.to_stream(stream, instance.mip_maps, (instance.num_mips,), Mipmap, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'zero', Uint64, (0, None), (False, None)
		yield 'data_size', Uint, (0, None), (False, None)
		yield 'width', Uint, (0, None), (False, None)
		yield 'height', Uint, (0, None), (False, None)
		yield 'depth', Uint, (0, None), (False, None)
		yield 'array_size', Uint, (0, None), (False, None)
		yield 'num_mips', Uint, (0, None), (False, None)
		if instance.context.version >= 20:
			yield 'unk_pz', Uint64, (0, None), (False, None)
		yield 'mip_maps', Array, ((instance.num_mips,), Mipmap, 0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'SizeInfoRaw [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zero = {self.fmt_member(self.zero, indent+1)}'
		s += f'\n	* data_size = {self.fmt_member(self.data_size, indent+1)}'
		s += f'\n	* width = {self.fmt_member(self.width, indent+1)}'
		s += f'\n	* height = {self.fmt_member(self.height, indent+1)}'
		s += f'\n	* depth = {self.fmt_member(self.depth, indent+1)}'
		s += f'\n	* array_size = {self.fmt_member(self.array_size, indent+1)}'
		s += f'\n	* num_mips = {self.fmt_member(self.num_mips, indent+1)}'
		s += f'\n	* unk_pz = {self.fmt_member(self.unk_pz, indent+1)}'
		s += f'\n	* mip_maps = {self.fmt_member(self.mip_maps, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
