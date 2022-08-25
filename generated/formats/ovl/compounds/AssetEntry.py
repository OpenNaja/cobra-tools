from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint


class AssetEntry(BaseStruct):

	"""
	refers to root entries so they can be grouped into set entries.
	It seems to point exclusively to RootEntry's whose Ext Hash is FF FF FF FF aka max uint32
	"""

	__name__ = AssetEntry

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
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
		super().set_defaults()
		self.file_hash = 0
		self.zero_0 = 0
		if self.context.version >= 19:
			self.ext_hash = 0
			self.zero_1 = 0
		self.file_index = 0
		self.zero_2 = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.file_hash = Uint.from_stream(stream, instance.context, 0, None)
		instance.zero_0 = Uint.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 19:
			instance.ext_hash = Uint.from_stream(stream, instance.context, 0, None)
			instance.zero_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.file_index = Uint.from_stream(stream, instance.context, 0, None)
		instance.zero_2 = Uint.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.file_hash)
		Uint.to_stream(stream, instance.zero_0)
		if instance.context.version >= 19:
			Uint.to_stream(stream, instance.ext_hash)
			Uint.to_stream(stream, instance.zero_1)
		Uint.to_stream(stream, instance.file_index)
		Uint.to_stream(stream, instance.zero_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'file_hash', Uint, (0, None), (False, None)
		yield 'zero_0', Uint, (0, None), (False, None)
		if instance.context.version >= 19:
			yield 'ext_hash', Uint, (0, None), (False, None)
			yield 'zero_1', Uint, (0, None), (False, None)
		yield 'file_index', Uint, (0, None), (False, None)
		yield 'zero_2', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'AssetEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* file_hash = {self.fmt_member(self.file_hash, indent+1)}'
		s += f'\n	* zero_0 = {self.fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* ext_hash = {self.fmt_member(self.ext_hash, indent+1)}'
		s += f'\n	* zero_1 = {self.fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* file_index = {self.fmt_member(self.file_index, indent+1)}'
		s += f'\n	* zero_2 = {self.fmt_member(self.zero_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
