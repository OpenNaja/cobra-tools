import logging
import traceback

from generated.base_struct import BaseStruct
from generated.formats.base.compounds.PadAlign import get_padding_size, get_padding
from generated.formats.manis.compounds.ManiBlock import ManiBlock


from generated.formats.manis.compounds.SubChunk import SubChunk
from generated.base_struct import BaseStruct


class SubChunkReader(BaseStruct):

	__name__ = 'SubChunkReader'

	_import_key = 'manis.compounds.SubChunkReader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

	@classmethod
	def read_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		for chunk_sizes in instance.arg:
			chunk_sizes.keys = ()
		for chunk_sizes in instance.arg:
			# start = stream.tell()
			chunk_sizes.keys = SubChunk.from_stream(stream, instance.context, chunk_sizes, None)
			# print(chunk_sizes)
			# print(chunk_sizes.keys)
			# subchunk_size =
			print(f"subchunk io_size {chunk_sizes.keys.io_size}")
			pad_size = get_padding_size(chunk_sizes.keys.io_size, alignment=8)
			chunk_sizes.padding = stream.read(pad_size)
			assert chunk_sizes.padding == b"\x00" * pad_size
			print(f"{chunk_sizes.padding} padding ends at {stream.tell()}")
			# break
			# break
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		for mani_info in instance.arg:
			ManiBlock.to_stream(mani_info.keys, stream, instance.context)
			for mb in mani_info.keys.repeats:
				stream.write(mb.data)
				stream.write(get_padding(mb.byte_size))
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def get_fields_str(cls, instance, indent=0):
		s = ''
		for chunk_sizes in instance.arg:
			s += str(chunk_sizes.keys)
		return s


