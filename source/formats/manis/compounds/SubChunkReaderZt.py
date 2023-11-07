# START_GLOBALS
from generated.base_struct import BaseStruct
from generated.formats.base.compounds.PadAlign import get_padding_size, get_padding


from generated.formats.manis.compounds.SubChunkZt import SubChunkZt
# END_GLOBALS


class SubChunkReaderZt(BaseStruct):

	# START_CLASS

	@classmethod
	def read_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		# for chunk_sizes in instance.arg:
		# 	chunk_sizes.keys = ()
		for chunk_sizes in instance.arg:
			chunk_sizes.keys = SubChunkZt.from_stream(stream, instance.context, chunk_sizes, None)
			# print(f"SubChunkZt io_size {chunk_sizes.keys.io_size}")
			pad_size = get_padding_size(chunk_sizes.keys.io_size, alignment=16)
			chunk_sizes.padding = stream.read(pad_size)
			assert chunk_sizes.padding == b"\x00" * pad_size
			# print(f"{chunk_sizes.padding} padding ends at {stream.tell()}")
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		for chunk_sizes in instance.arg:
			SubChunkZt.to_stream(chunk_sizes.keys, stream, instance.context)
			stream.write(get_padding(chunk_sizes.keys.io_size, alignment=8))
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def get_fields_str(cls, instance, indent=0):
		s = ''
		for chunk_sizes in instance.arg:
			s += str(chunk_sizes.keys)
		return s

