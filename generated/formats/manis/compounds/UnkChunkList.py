from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.base.compounds.PadAlign import PadAlign
from generated.formats.manis.compounds.ChunkSizes import ChunkSizes
from generated.formats.manis.compounds.SubChunkReader import SubChunkReader
from generated.formats.ovl_base.compounds.Empty import Empty
from generated.formats.ovl_base.compounds.SmartPadding import SmartPadding


class UnkChunkList(BaseStruct):

	__name__ = 'UnkChunkList'

	_import_key = 'manis.compounds.UnkChunkList'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ref = Empty(self.context, 0, None)
		self.zero_0 = SmartPadding(self.context, 0, None)
		self.subchunk_count = 0
		self.flag = 0
		self.zero_1 = 0
		self.chunksize_list = Array(self.context, 0, None, (0,), ChunkSizes)
		self.subchunk_list = SubChunkReader(self.context, self.chunksize_list, None)

		# ?
		self.pad = PadAlign(self.context, 16, self.ref)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('ref', Empty, (0, None), (False, None), None)
		yield ('zero_0', SmartPadding, (0, None), (False, None), None)
		yield ('subchunk_count', Ushort, (0, None), (False, None), None)
		yield ('flag', Ushort, (0, None), (False, None), None)
		yield ('zero_1', Uint, (0, None), (False, None), None)
		yield ('chunksize_list', Array, (0, None, (None,), ChunkSizes), (False, None), None)
		yield ('subchunk_list', SubChunkReader, (None, None), (False, None), None)
		yield ('pad', PadAlign, (16, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ref', Empty, (0, None), (False, None)
		yield 'zero_0', SmartPadding, (0, None), (False, None)
		yield 'subchunk_count', Ushort, (0, None), (False, None)
		yield 'flag', Ushort, (0, None), (False, None)
		yield 'zero_1', Uint, (0, None), (False, None)
		yield 'chunksize_list', Array, (0, None, (instance.subchunk_count,), ChunkSizes), (False, None)
		yield 'subchunk_list', SubChunkReader, (instance.chunksize_list, None), (False, None)
		yield 'pad', PadAlign, (16, instance.ref), (False, None)


UnkChunkList.init_attributes()
