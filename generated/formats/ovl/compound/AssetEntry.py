from generated.formats.base.basic import fmt_member
from generated.formats.base.basic import Uint
from generated.struct import StructBase


class AssetEntry(StructBase):

	"""
	refers to root entries so they can be grouped into set entries.
	It seems to point exclusively to RootEntry's whose Ext Hash is FF FF FF FF aka max uint32
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.file_hash = 0
		self.zero_0 = 0
		self.ext_hash = 0
		self.zero_1 = 0

		# index into root entries array; hash of targeted file matches this assetentry's hash.
		self.file_index = 0
		self.zero_2 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.file_hash = 0
		self.zero_0 = 0
		if self.context.version >= 19:
			self.ext_hash = 0
			self.zero_1 = 0
		self.file_index = 0
		self.zero_2 = 0

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
		instance.file_hash = stream.read_uint()
		instance.zero_0 = stream.read_uint()
		if instance.context.version >= 19:
			instance.ext_hash = stream.read_uint()
			instance.zero_1 = stream.read_uint()
		instance.file_index = stream.read_uint()
		instance.zero_2 = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.file_hash)
		stream.write_uint(instance.zero_0)
		if instance.context.version >= 19:
			stream.write_uint(instance.ext_hash)
			stream.write_uint(instance.zero_1)
		stream.write_uint(instance.file_index)
		stream.write_uint(instance.zero_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('file_hash', Uint, (0, None))
		yield ('zero_0', Uint, (0, None))
		if instance.context.version >= 19:
			yield ('ext_hash', Uint, (0, None))
			yield ('zero_1', Uint, (0, None))
		yield ('file_index', Uint, (0, None))
		yield ('zero_2', Uint, (0, None))

	def get_info_str(self, indent=0):
		return f'AssetEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* file_hash = {fmt_member(self.file_hash, indent+1)}'
		s += f'\n	* zero_0 = {fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* ext_hash = {fmt_member(self.ext_hash, indent+1)}'
		s += f'\n	* zero_1 = {fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* file_index = {fmt_member(self.file_index, indent+1)}'
		s += f'\n	* zero_2 = {fmt_member(self.zero_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
