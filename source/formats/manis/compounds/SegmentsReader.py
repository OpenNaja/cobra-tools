# START_GLOBALS
import logging

from generated.base_struct import BaseStruct
from generated.formats.base.compounds.PadAlign import get_padding
from modules.formats.shared import get_padding_size

# END_GLOBALS


class SegmentsReader(BaseStruct):

	# START_CLASS

	@classmethod
	def read_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		# print(instance.context)
		for segment in instance.arg:
			segment.data = stream.read(segment.byte_size)
			pad_size = get_padding_size(segment.byte_size)
			segment.padding = stream.read(pad_size)
			assert segment.padding == b"\x00" * pad_size
		logging.info(f"Compressed keys data ends at {stream.tell()}")
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		for segment in instance.arg:
			stream.write(segment.data)
			stream.write(get_padding(segment.byte_size))
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def get_fields_str(cls, instance, indent=0):
		s = ''
		for mani_info in instance.arg:
			if hasattr(mani_info, "keys"):
				s += str(mani_info.keys)
		return s

