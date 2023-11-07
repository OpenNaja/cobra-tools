from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class UnkChunkListZT(BaseStruct):

	__name__ = 'UnkChunkListZT'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ref = name_type_map['Empty'](self.context, 0, None)
		self.subchunk_count = name_type_map['Uint64'](self.context, 0, None)
		self.pad_1 = name_type_map['Uint64'](self.context, 0, None)
		self.chunksize_list = Array(self.context, 0, None, (0,), name_type_map['ChunkSizesZT'])
		self.pad_2 = name_type_map['Uint64'](self.context, 0, None)
		self.subchunk_list = name_type_map['SubChunkReaderZt'](self.context, self.chunksize_list, None)

		# ?
		self.unk_chunk_list_z_t_pad = name_type_map['PadAlign'](self.context, 16, self.ref)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ref', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'subchunk_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'pad_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'chunksize_list', Array, (0, None, (None,), name_type_map['ChunkSizesZT']), (False, None), (None, None)
		yield 'pad_2', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'subchunk_list', name_type_map['SubChunkReaderZt'], (None, None), (False, None), (None, None)
		yield 'unk_chunk_list_z_t_pad', name_type_map['PadAlign'], (16, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None)
		yield 'subchunk_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'pad_1', name_type_map['Uint64'], (0, None), (False, None)
		yield 'chunksize_list', Array, (0, None, (instance.subchunk_count,), name_type_map['ChunkSizesZT']), (False, None)
		yield 'pad_2', name_type_map['Uint64'], (0, None), (False, None)
		yield 'subchunk_list', name_type_map['SubChunkReaderZt'], (instance.chunksize_list, None), (False, None)
		yield 'unk_chunk_list_z_t_pad', name_type_map['PadAlign'], (16, instance.ref), (False, None)
