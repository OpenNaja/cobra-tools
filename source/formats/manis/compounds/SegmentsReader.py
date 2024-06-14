# START_GLOBALS
import logging

from generated.base_struct import BaseStruct
from modules.formats.shared import get_padding_size

# END_GLOBALS


class SegmentsReader(BaseStruct):

	# START_CLASS

	@classmethod
	def read_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		for segment in instance.arg:
			cls.pad_to_start(instance, stream)
			try:
				segment.data = stream.read(segment.byte_size)
			except:
				logging.exception(f"segment.data failed")
		# logging.debug(f"Compressed keys data ends at {stream.tell()}")
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def pad_to_start(cls, instance, stream):
		pad_size = get_padding_size(stream.tell() - instance.io_start)
		padding = stream.read(pad_size)
		if padding != b"\x00" * pad_size:
			logging.warning(f"Segment padding is not 00: '{padding}' at {stream.tell()}")

	@classmethod
	def align_to(cls, instance, stream, alignment=16, rel=None):
		abs_offset = stream.tell()
		relative_offset = abs_offset - instance.io_start
		padding_len = get_padding_size(relative_offset, alignment=alignment)
		# logging.debug(f"Aligning to {alignment} from {abs_offset} to {abs_offset+padding_len} ({padding_len} bytes)")
		stream.write(b'\x00' * padding_len)

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		for segment in instance.arg:
			cls.align_to(instance, stream)
			stream.write(segment.data)
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def get_fields_str(cls, instance, indent=0):
		s = ''
		for mani_info in instance.arg:
			if hasattr(mani_info, "keys"):
				s += str(mani_info.keys)
		return s

