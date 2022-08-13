from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Mipmap(MemStruct):

	"""
	Describes one tex mipmap
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

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
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield 'offset', Uint, (0, None)
		yield 'size', Uint, (0, None)
		yield 'size_array', Uint, (0, None)
		yield 'size_scan', Uint, (0, None)
		yield 'size_data', Uint, (0, None)

	def get_info_str(self, indent=0):
		return f'Mipmap [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* offset = {self.fmt_member(self.offset, indent+1)}'
		s += f'\n	* size = {self.fmt_member(self.size, indent+1)}'
		s += f'\n	* size_array = {self.fmt_member(self.size_array, indent+1)}'
		s += f'\n	* size_scan = {self.fmt_member(self.size_scan, indent+1)}'
		s += f'\n	* size_data = {self.fmt_member(self.size_data, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
