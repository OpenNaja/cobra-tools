# START_GLOBALS
import logging
from generated.base_struct import BaseStruct
from generated.formats.manis.structs.CompressedHeader import CompressedHeader

# END_GLOBALS


class KeysReader(BaseStruct):

	# START_CLASS

	@classmethod
	def read_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		if cls.get_compressed_manis(instance):
			instance.data = CompressedHeader.from_stream(stream, instance.context)
		else:
			instance.data = None
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def get_compressed_manis(cls, instance):
		return [mani_info for mani_info in instance.arg if mani_info.dtype != 0]

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		if cls.get_compressed_manis(instance):
			CompressedHeader.to_stream(instance.data, stream, instance.context)
		instance.io_size = stream.tell() - instance.io_start

