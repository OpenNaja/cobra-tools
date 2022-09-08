import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ms2.compounds.StreamsZTHeader import StreamsZTHeader


class Buffer0(BaseStruct):

	__name__ = 'Buffer0'

	_import_path = 'generated.formats.ms2.compounds.Buffer0'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# djb2 hashes
		self.name_hashes = Array(self.context, 0, None, (0,), Uint)

		# names
		self.names = Array(self.context, 0, None, (0,), ZString)

		# align to 4
		self.names_padding = Array(self.context, 0, None, (0,), Ubyte)
		self.zt_streams_header = StreamsZTHeader(self.context, self.arg, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'name_hashes', Array, (0, None, (instance.arg.name_count,), Uint), (False, None)
		yield 'names', Array, (0, None, (instance.arg.name_count,), ZString), (False, None)
		if instance.context.version >= 50:
			yield 'names_padding', Array, (0, None, ((4 - (instance.names.io_size % 4)) % 4,), Ubyte), (False, None)
		if instance.context.version <= 13:
			yield 'zt_streams_header', StreamsZTHeader, (instance.arg, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Buffer0 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
