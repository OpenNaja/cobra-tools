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

	_import_key = 'manis.compounds.InfoHeader'

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

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'version', Uint, (0, None), (False, None)
		yield 'mani_count', Uint, (0, None), (False, None)
		yield 'names', Array, (0, None, (instance.mani_count,), ZString), (False, None)
		yield 'header', SizedStrData, (0, None), (False, None)
		yield 'mani_infos', Array, (0, None, (instance.mani_count,), ManiInfo), (False, None)
		yield 'name_buffer', Buffer1, (int(instance.header.hash_block_size / 4), None), (False, None)
		yield 'keys_buffer', KeysReader, (instance.mani_infos, None), (False, None)
