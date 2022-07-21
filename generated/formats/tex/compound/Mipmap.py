from source.formats.base.basic import fmt_member
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class Mipmap(MemStruct):

	"""
	Describes one tex mipmap
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default=False)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# starting offset into the texture buffer for this mip level
		self.offset = 0

		# bytes for one array entry
		self.size = 0

		# bytes for all array entries
		self.size_array = 0

		# size of a scan line of blocks, including padding that is added to the end of the line
		self.size_scan = 0

		# size of the non-empty scanline blocks, ie. the last lods add empty scanlines as this is smaller than size
		self.size_data = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.offset = 0
		self.size = 0
		self.size_array = 0
		self.size_scan = 0
		self.size_data = 0

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
		instance.offset = stream.read_uint()
		instance.size = stream.read_uint()
		instance.size_array = stream.read_uint()
		instance.size_scan = stream.read_uint()
		instance.size_data = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.offset)
		stream.write_uint(instance.size)
		stream.write_uint(instance.size_array)
		stream.write_uint(instance.size_scan)
		stream.write_uint(instance.size_data)

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
		return f'Mipmap [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* size = {fmt_member(self.size, indent+1)}'
		s += f'\n	* size_array = {fmt_member(self.size_array, indent+1)}'
		s += f'\n	* size_scan = {fmt_member(self.size_scan, indent+1)}'
		s += f'\n	* size_data = {fmt_member(self.size_data, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
