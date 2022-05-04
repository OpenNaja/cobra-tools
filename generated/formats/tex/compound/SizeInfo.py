from source.formats.base.basic import fmt_member
from generated.array import Array
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.tex.compound.Mipmap import Mipmap


class SizeInfo(MemStruct):

	"""
	Data struct for headers of type 7
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

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
		instance.zero = stream.read_uint64()
		instance.data_size = stream.read_uint()
		instance.width = stream.read_uint()
		instance.height = stream.read_uint()
		instance.depth = stream.read_uint()
		instance.array_size = stream.read_uint()
		instance.num_mips = stream.read_uint()
		if instance.context.version >= 20:
			instance.unk_pz = stream.read_uint64()
		instance.mip_maps = Array.from_stream(stream, (instance.num_mips,), Mipmap, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64(instance.zero)
		stream.write_uint(instance.data_size)
		stream.write_uint(instance.width)
		stream.write_uint(instance.height)
		stream.write_uint(instance.depth)
		stream.write_uint(instance.array_size)
		stream.write_uint(instance.num_mips)
		if instance.context.version >= 20:
			stream.write_uint64(instance.unk_pz)
		Array.to_stream(stream, instance.mip_maps, (instance.num_mips,), Mipmap, instance.context, 0, None)

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
		return f'SizeInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		s += f'\n	* data_size = {fmt_member(self.data_size, indent+1)}'
		s += f'\n	* width = {fmt_member(self.width, indent+1)}'
		s += f'\n	* height = {fmt_member(self.height, indent+1)}'
		s += f'\n	* depth = {fmt_member(self.depth, indent+1)}'
		s += f'\n	* array_size = {fmt_member(self.array_size, indent+1)}'
		s += f'\n	* num_mips = {fmt_member(self.num_mips, indent+1)}'
		s += f'\n	* unk_pz = {fmt_member(self.unk_pz, indent+1)}'
		s += f'\n	* mip_maps = {fmt_member(self.mip_maps, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
