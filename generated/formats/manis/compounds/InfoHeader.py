from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.manis.compounds.Buffer1 import Buffer1
from generated.formats.manis.compounds.KeysReader import KeysReader
from generated.formats.manis.compounds.ManiInfo import ManiInfo
from generated.formats.manis.compounds.SizedStrData import SizedStrData


class InfoHeader(BaseStruct):

	"""
	Custom header struct
	"""

	__name__ = 'InfoHeader'

	_import_path = 'generated.formats.manis.compounds.InfoHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.version = 0
		self.mani_count = 0
		self.names = Array(self.context, 0, None, (0,), ZString)
		self.header = SizedStrData(self.context, 0, None)
		self.mani_infos = Array(self.context, 0, None, (0,), ManiInfo)
		self.name_buffer = Buffer1(self.context, int(self.header.hash_block_size / 4), None)
		self.keys_buffer = KeysReader(self.context, self.mani_infos, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.version = 0
		self.mani_count = 0
		self.names = Array(self.context, 0, None, (self.mani_count,), ZString)
		self.header = SizedStrData(self.context, 0, None)
		self.mani_infos = Array(self.context, 0, None, (self.mani_count,), ManiInfo)
		self.name_buffer = Buffer1(self.context, int(self.header.hash_block_size / 4), None)
		self.keys_buffer = KeysReader(self.context, self.mani_infos, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.version = Uint.from_stream(stream, instance.context, 0, None)
		instance.context.version = instance.version
		instance.mani_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.names = Array.from_stream(stream, instance.context, 0, None, (instance.mani_count,), ZString)
		instance.header = SizedStrData.from_stream(stream, instance.context, 0, None)
		instance.mani_infos = Array.from_stream(stream, instance.context, 0, None, (instance.mani_count,), ManiInfo)
		instance.name_buffer = Buffer1.from_stream(stream, instance.context, int(instance.header.hash_block_size / 4), None)
		instance.keys_buffer = KeysReader.from_stream(stream, instance.context, instance.mani_infos, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.version)
		Uint.to_stream(stream, instance.mani_count)
		Array.to_stream(stream, instance.names, instance.context, 0, None, (instance.mani_count,), ZString)
		SizedStrData.to_stream(stream, instance.header)
		Array.to_stream(stream, instance.mani_infos, instance.context, 0, None, (instance.mani_count,), ManiInfo)
		Buffer1.to_stream(stream, instance.name_buffer)
		KeysReader.to_stream(stream, instance.keys_buffer)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'version', Uint, (0, None), (False, None)
		yield 'mani_count', Uint, (0, None), (False, None)
		yield 'names', Array, (0, None, (instance.mani_count,), ZString), (False, None)
		yield 'header', SizedStrData, (0, None), (False, None)
		yield 'mani_infos', Array, (0, None, (instance.mani_count,), ManiInfo), (False, None)
		yield 'name_buffer', Buffer1, (int(instance.header.hash_block_size / 4), None), (False, None)
		yield 'keys_buffer', KeysReader, (instance.mani_infos, None), (False, None)

	def get_info_str(self, indent=0):
		return f'InfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* version = {self.fmt_member(self.version, indent+1)}'
		s += f'\n	* mani_count = {self.fmt_member(self.mani_count, indent+1)}'
		s += f'\n	* names = {self.fmt_member(self.names, indent+1)}'
		s += f'\n	* header = {self.fmt_member(self.header, indent+1)}'
		s += f'\n	* mani_infos = {self.fmt_member(self.mani_infos, indent+1)}'
		s += f'\n	* name_buffer = {self.fmt_member(self.name_buffer, indent+1)}'
		s += f'\n	* keys_buffer = {self.fmt_member(self.keys_buffer, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
