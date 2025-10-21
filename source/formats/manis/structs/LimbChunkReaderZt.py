# START_GLOBALS
from generated.base_struct import BaseStruct
from generated.formats.base.structs.PadAlign import get_padding_size, get_padding
import logging

from generated.formats.manis.structs.LimbChunkZt import LimbChunkZt
# END_GLOBALS


class LimbChunkReaderZt(BaseStruct):

	# START_CLASS

	@classmethod
	def read_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		# for chunk_sizes in instance.arg:
		# 	chunk_sizes.keys = ()
		for chunk_sizes in instance.arg:
			# cls.pad_to_start(instance, stream)
			chunk_sizes.keys = LimbChunkZt.from_stream(stream, instance.context, chunk_sizes, None)
			# cls.pad_to_start(instance, stream)
			# print(f"LimbChunkZt io_size {chunk_sizes.keys.io_size}")
			# todo this loses alignment
			# pad_size = get_padding_size(chunk_sizes.keys.io_size, alignment=16)
			# chunk_sizes.padding = stream.read(pad_size)
			# assert chunk_sizes.padding == b"\x00" * pad_size
			# print(f"{chunk_sizes.padding} padding ends at {stream.tell()}")
		instance.io_size = stream.tell() - instance.io_start


	@classmethod
	def pad_to_start(cls, instance, stream):
		pad_size = get_padding_size(stream.tell() - instance.io_start)
		padding = stream.read(pad_size)
		if padding != b"\x00" * pad_size:
			logging.warning(f"Segment padding is not 00: '{padding}' at {stream.tell()}")

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		for chunk_sizes in instance.arg:
			LimbChunkZt.to_stream(chunk_sizes.keys, stream, instance.context)
			stream.write(get_padding(chunk_sizes.keys.io_size, alignment=8))
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def get_fields_str(cls, instance, indent=0):
		s = ''
		for chunk_sizes in instance.arg:
			s += str(chunk_sizes.keys)
		return s

