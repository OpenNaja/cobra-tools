# START_GLOBALS
import logging

from generated.base_struct import BaseStruct
from generated.formats.base.compounds.PadAlign import get_padding
from generated.formats.manis.compounds.CompressedManiData import CompressedManiData
from generated.formats.manis.compounds.ManiBlock import ManiBlock
from generated.formats.manis.compounds.UnkChunkList import UnkChunkList
from modules.formats.shared import get_padding_size

# END_GLOBALS


class KeysReader(BaseStruct):

	# START_CLASS

	@classmethod
	def read_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		# print(instance.context)
		for mani_info in instance.arg:
			logging.info(mani_info)
			mani_block_start = stream.tell()
			logging.info(f"Reading keys block at {mani_block_start}")
			# if mani_block_start == 964833:
			# 	break
			try:
				mani_info.keys = ManiBlock.from_stream(stream, instance.context, mani_info, None)
				# logging.info(mani_info.keys)

				if isinstance(mani_info.keys.key_data, CompressedManiData):
					for mb in mani_info.keys.key_data.repeats:
						mb.data = stream.read(mb.byte_size)
						pad_size = get_padding_size(mb.byte_size)
						mb.padding = stream.read(pad_size)
						assert mb.padding == b"\x00" * pad_size
					logging.info(f"Compressed keys data ends at {stream.tell()}")
				else:
					logging.info(f"Uncompressed keys data ends at {stream.tell()}")
				# probably used in the high JWE2 types, but apparently also in PZ crane, even after uncompressed data
				if mani_info.dtype.has_list or mani_info.dtype.unk:
					# if isinstance(mani_info.keys.key_data, CompressedManiData) and mani_info.keys.key_data.count > 0:
					mani_info.subchunks = UnkChunkList.from_stream(stream, instance.context, mani_info, None)
					logging.info(mani_info.subchunks)
				# break
			except:
				logging.exception(f"Reading ManiBlock failed at {mani_block_start} for {mani_info}")
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		for mani_info in instance.arg:
			if mani_info.dtype != 70 and mani_info.count_a > 0 and mani_info.count_b > 0:
				ManiBlock.to_stream(mani_info.keys, stream, instance.context)
				if isinstance(mani_info.keys.key_data, CompressedManiData):
					for mb in mani_info.keys.key_data.repeats:
						stream.write(mb.data)
						stream.write(get_padding(mb.byte_size))
				# if (mani_info.keys.count > 0) and (mani_info.dtype > 5):
				# 	UnkChunkList.to_stream(mani_info.subchunks, stream, mani_info.subchunks.context)
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def get_fields_str(cls, instance, indent=0):
		s = ''
		for mani_info in instance.arg:
			if hasattr(mani_info, "keys"):
				s += str(mani_info.keys)
		return s

